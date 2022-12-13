from typing import Optional
import torch
from torch import nn
from transformers.models.roberta.modeling_roberta import (
    RobertaPreTrainedModel,
    RobertaModel,
    RobertaConfig,
    RobertaEncoder
)
from transformers.modeling_outputs import SequenceClassifierOutput


class RobertaForSentimentAnalysisV1(RobertaPreTrainedModel):
    config_class = RobertaConfig
    base_model_prefix = "roberta"

    def __init__(self, config):
        super(RobertaForSentimentAnalysisV1, self).__init__(config)
        self.num_labels = config.num_labels
        self.roberta = RobertaModel(config)
        self.qa_outputs = nn.Linear(config.hidden_size, config.num_labels)

        self.init_weights()

    def forward(self, input_ids,
                attention_mask=None,
                token_type_ids=None,
                position_ids=None,
                head_mask=None,
                start_positions=None,
                end_positions=None,
                labels: Optional[torch.LongTensor] = None,
                ):

        out = self.roberta(input_ids,
                           attention_mask=attention_mask,
                           # token_type_ids=token_type_ids,
                           position_ids=position_ids,
                           head_mask=head_mask,
                           )
        cls_output = out.last_hidden_state[:, 0, :]
        logits = self.qa_outputs(cls_output)
        
        return SequenceClassifierOutput(
            loss=None,
            logits=logits,
            hidden_states=out.hidden_states,
            attentions=out.attentions,
        )


class RobertaForSentimentAnalysisV2(RobertaPreTrainedModel):
    config_class = RobertaConfig
    base_model_prefix = "roberta"

    def __init__(self, config):
        super(RobertaForSentimentAnalysisV2, self).__init__(config)
        self.num_labels = config.num_labels
        self.roberta = RobertaModel(config)
        self.qa_outputs = nn.Linear(4*config.hidden_size, config.num_labels)

        self.init_weights()

    def forward(self, input_ids,
                attention_mask=None,
                token_type_ids=None,
                position_ids=None,
                head_mask=None,
                start_positions=None,
                end_positions=None,
                labels: Optional[torch.LongTensor] = None,
                ):

        out = self.roberta(input_ids,
                           attention_mask=attention_mask,
                           # token_type_ids=token_type_ids,
                           position_ids=position_ids,
                           head_mask=head_mask,
                           output_hidden_states=True)
        # cls_output = torch.cat((outputs[2][-1][:, 0, ...], outputs[2][-2][:, 0, ...],
        #                        outputs[2][-3][:, 0, ...], outputs[2][-4][:, 0, ...]), -1)
        cls_output = torch.cat((out.hidden_states[-1][:, 0, :],
                                out.hidden_states[-2][:, 0, :],
                                out.hidden_states[-3][:, 0, :],
                                out.hidden_states[-4][:, 0, :]), -1)
        logits = self.qa_outputs(cls_output)

        del out.hidden_states

        return SequenceClassifierOutput(
            loss=None,
            logits=logits,
            hidden_states=None,
            attentions=out.attentions,
        )
