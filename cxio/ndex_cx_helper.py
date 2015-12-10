import time
from cxio.element import Element
from cxio.aspect_element import AspectElement
from cxio.cx_constants import CxConstants
from cxio.aspect_element import AspectElement
from cxio.cx_reader import CxReader
from cxio.cx_writer import CxWriter
from cxio.cx_constants import CxConstants
from cxio.cx_util import CxUtil
from cxio.element_maker import ElementMaker


class NdexCXHelper:

    def __init__(self, output_stream):
        self.contexts = {}
        self.citation_id_counter = 0
        self.support_id_counter = 0
        self.edge_id_counter = 0
        self.node_id_counter = 0
        self.update_time = -1
        self.cx_writer = CxWriter(output_stream)
        self.aspect_names = ["@context", "citations", "edgeAttributes",
                             "edgeCitations", "edgeSupports", "edges",
                             "networkAttributes", "nodeAttributes", "nodeCitations",
                             "nodeSupports", "nodes", "provenanceHistory", "supports"]

    def start(self):
        self.update_time = int(round(time.time() * 1000))
        self.__add_pre_metadata()
        self.cx_writer.start()

    def end(self):
        self.__add_post_metadata()
        self.cx_writer.end()

    def add_cx_context(self, prefix, uri):
        self.contexts[prefix] = uri

    def emit_cx_context(self):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_context_element(self.contexts))

    def emit_cx_citation(self, citation_type, title, contributors, identifier, description):
        self.citation_id_counter += 1
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_citation_aspect_element(self.citation_id_counter, citation_type, title,
                                                             contributors, identifier, description))
        return self.citation_id_counter

    def emit_cx_support(self, cx_citation_id, text):
        self.support_id_counter += 1
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_support_aspect_element(self.support_id_counter, cx_citation_id, text))
        return self.support_id_counter

    def emit_cx_edge(self, source_id, target_id, interaction):
        self.edge_id_counter += 1
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_edges_aspect_element(self.edge_id_counter, source_id,
                                                     target_id, interaction))
        return self.edge_id_counter

    def emit_cx_edge_attribute(self, edge_id, name, value):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_edge_attributes_aspect_element(edge_id, name, value))

    def emit_cx_node(self, node_name):
        self.node_id_counter += 1
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_nodes_aspect_element(self.node_id_counter, node_name))
        return self.node_id_counter

    def emit_cx_node_attribute(self, node_id, name, value, att_type=None):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_node_attributes_aspect_element(node_id, name, value, att_type))

    def emit_cx_function_term(self, function_term):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_function_term_aspect_element(function_term))

    def emit_cx_node_citation(self, node_id, citation_id):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_node_citation_aspect_element(node_id, citation_id))

    def emit_cx_edge_citation(self, edge_id, citation_id):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_edge_citation_aspect_element(edge_id, citation_id))

    def emit_cx_node_support(self, node_id, support_id):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_node_support_aspect_element(node_id, support_id))

    def emit_cx_edge_support(self, edge_id, support_id):
        self.cx_writer.write_single_aspect_fragment(
            ElementMaker.create_ndex_edge_support_aspect_element(edge_id, support_id))

    def __add_pre_metadata(self):
        pre_meta_data = []
        for aspect_name in self.aspect_names:
            pre_meta_data.append(ElementMaker.create_pre_metadata_element(aspect_name, 1, '1.0', self.update_time))
        self.cx_writer.add_pre_meta_data(pre_meta_data)

    def __add_post_metadata(self):
        post_meta_data = [
            ElementMaker.create_post_metadata_element('nodes', self.node_id_counter),
            ElementMaker.create_post_metadata_element('edges', self.edge_id_counter),
            ElementMaker.create_post_metadata_element('supports', self.support_id_counter),
            ElementMaker.create_post_metadata_element('citations', self.citation_id_counter)
        ]
        self.cx_writer.add_post_meta_data(post_meta_data)