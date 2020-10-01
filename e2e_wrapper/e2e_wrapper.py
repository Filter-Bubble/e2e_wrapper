# -*- coding: utf-8 -*-
from . import __version__
import logging

import e2edutch.coref_model
import KafNafParserPy
from KafNafParserPy import KafNafParser
from lxml.etree import XMLSyntaxError
from io import BytesIO
import sys
from itertools import groupby
from operator import itemgetter
from xml.sax.saxutils import escape
import tensorflow as tf

logger = logging.getLogger(__name__)
this_name = 'Coreference resolution based on e2e model'

def get_naf(input_file):

    input = input_file.read()
    try:
        naf = KafNafParser(BytesIO(input))
    except XMLSyntaxError:
        input = input.decode("utf-8")
        if "<NAF" in input and "</NAF>" in input:
            # I'm guessing this should be a NAF file but something is wrong
            logging.exception("Error parsing NAF file")
            raise
        naf = KafNafParser(type="NAF")
        naf.set_version("3.0")
        naf.set_language("nl")
        naf.lang = "nl"
        naf.raw = input
        naf.set_raw(naf.raw)
    return naf


def create_text_layer(st_doc, knaf_obj):
    id_to_tokenid = {}
    wcount = 1
    offsets = {}
    txt = knaf_obj.get_raw()
    for sid, sentence in enumerate(st_doc.sentences):
        id_to_tokenid[sid+1] = {}
        for token in sentence.tokens:
            token_obj = KafNafParserPy.Cwf(type=knaf_obj.get_type())
            token_id = 'w{}'.format(wcount)
            token_length = len(token.text)
            offsets[wcount] = txt.find(token.text, offsets.get(wcount-1, 0))
            token_obj.set_id(token_id)
            token_obj.set_length(str(token_length))
            # token_obj.set_offset(str(offset)) # Is this correct????
            token_obj.set_para('1')
            token_obj.set_sent(str(sid+1))
            token_obj.set_text(token.text)
            token_obj.set_offset(str(offsets[wcount]))

            wcount += 1
            id_to_tokenid[sid+1][token.id] = token_id
            knaf_obj.add_wf(token_obj)
    return id_to_tokenid


def create_coref_layer(knaf_obj):
    return knaf_obj



def add_linguistic_processors(in_obj):
    name = this_name

    my_lp = KafNafParserPy.Clp()
    my_lp.set_name(name)
    my_lp.set_version(__version__)
    my_lp.set_timestamp()
    in_obj.add_linguistic_processor('coreferences', my_lp)

    return in_obj

def get_jsonlines(knaf_obj):
    jsonlines_obj = []
    # TODO
    return jsonlines_obj

def parse(input_file, cfg_file, model_name='best'):
    if isinstance(input_file, KafNafParser):
        knaf_obj = input_file
    else:
        knaf_obj = get_naf(input_file)

    jsonlines_obj = get_jsonlines(knaf_obj)

    lang = knaf_obj.get_language()
    if lang != 'nl':
        logging.warning('ERROR! Language is {} and must be nl (Dutch)'
                        .format(lang))
        sys.exit(-1)

    config = e2edutch.util.initialize_from_env(model_name, cfg_file)
    model = e2edutch.coref_model.CorefModel(config)
    with tf.Session() as session:
        model.restore(session)

        tensorized_example = model.tensorize_example(
                jsonlines_obj, is_training=False)
        feed_dict = {i: t for i, t in zip(
            model.input_tensors, tensorized_example)}
        _, _, _, top_span_starts, top_span_ends, top_antecedents, top_antecedent_scores = session.run(
            model.predictions, feed_dict=feed_dict)
        predicted_antecedents = model.get_predicted_antecedents(
            top_antecedents, top_antecedent_scores)
        jsonlines_obj["predicted_clusters"], _ = model.get_predicted_clusters(
            top_span_starts, top_span_ends, predicted_antecedents)
        # TODO convert back to knaf





    in_obj = add_linguistic_processors(in_obj)
    return in_obj
