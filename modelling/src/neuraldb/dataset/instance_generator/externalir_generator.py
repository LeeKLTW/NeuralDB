import itertools
import logging

from neuraldb.dataset.instance_generator.instance_generator import InstanceGenerator

logger = logging.getLogger(__name__)


class ExternalIRGenerator(InstanceGenerator):
    def _process_query(self, query_obj, update_tokens):
        query_tokens = self.tokenizer.tokenize("Answer question: " + query_obj["query"])
        answer_tokens = [
            self.maybe_tokenize_answer(answer) for answer in query_obj["answer"]
        ]

        facts = set(itertools.chain(*query_obj["predicted_facts"]))
        context_tokens = [update_tokens[fact] for fact in facts][:10]

        yield self.maybe_decorate_with_metadata(
            {
                "query": query_tokens,
                "context": context_tokens,
                "output": self.concatenate_answer(answer_tokens),
            },
            query_obj,
        )
