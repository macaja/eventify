import torch

from transformers import (
    DistilBertTokenizer, DistilBertModel,
    BertTokenizer, BertModel,
    RobertaTokenizer, RobertaModel,
    # Add more models as needed
)

class BaseModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def load_model(self):
        if self.model_name == 'distilbert':
            self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
            self.model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        elif self.model_name == 'bert':
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
        elif self.model_name == 'roberta':
            self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
            self.model = RobertaModel.from_pretrained('roberta-base')
        # Add more models as needed

    def get_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        outputs = self.model(**inputs)
        embeddings = torch.mean(outputs.last_hidden_state, dim=1).detach()
        return embeddings.squeeze(0)

class ModelFactory:
    def __init__(self):
        self.models = {}

    def get_model(self, model_name):
        if model_name not in self.models:
            self.models[model_name] = BaseModel(model_name)
            self.models[model_name].load_model()
        return self.models[model_name]