import torch
import torch.nn as nn
from torch import Tensor
from torch import optim
import torch.nn.functional as F

class RNN(nn.Module):
    def __init__(self, data_name, hidden_size, embedding, num_classes,use_embedding=False, num_layer = 1, train_embedding=True):
        super(RNN, self).__init__()
        self.data_name = data_name
        self.use_cuda = torch.cuda.is_available()
        self.hidden_size = hidden_size

        if use_embedding:
            self.embedding = nn.Embedding(embedding.shape[0], embedding.shape[1])
            self.embedding.weight = nn.Parameter(embedding)
            self.input_size = embedding.shape[1] # V - Size of embedding vector

        else:
            self.embedding = nn.Embedding(embedding[0], embedding[1])
            self.input_size = embedding[1]

        self.embedding.weight.requires_grad = train_embedding

        self.lstm = nn.LSTM(self.input_size, self.hidden_size, num_layers=num_layer, bidirectional=False)

        self.classifier = nn.Sequential(
            nn.Linear(hidden_size * 4, 256),
            nn.Dropout(),
            nn.Linear(256, num_classes)
        )

    def forward(self, input, hidden):
        '''
        input           -> ( Max. Sequence Length (per batch) x Batch Size)
        hidden          -> ( Num. Layers * Num. Directions x Batch Size x Hidden Size)
        '''
        embedded = self.embedding(input) # L, B, V

        batch_size = embedded.size()[1]

        outputs, hidden = self.lstm(embedded, hidden)
        cats = torch.cat([outputs[0], outputs[-1]], dim=1)
        pred = self.classifier(cats)

        return pred

    def init_weights(self):
        ''' Initialize weights of lstm 1 '''
        for name_1, param_1 in self.lstm_1.named_parameters():
            if 'bias' in name_1:
                nn.init.constant_(param_1, 0.0)
            elif 'weight' in name_1:
                nn.init.xavier_normal_(param_1)

        ''' Set weights of lstm 2 identical to lstm 1 '''
        lstm_1 = self.lstm_1.state_dict()
        lstm_2 = self.lstm_2.state_dict()

        for name_1, param_1 in lstm_1.items():
            # Backwards compatibility for serialized parameters.
            if isinstance(param_1, torch.nn.Parameter):
                param_1 = param_1.data

            lstm_2[name_1].copy_(param_1)

    def init_hidden(self, batch_size):
        # Hidden dimensionality : 2 (h_0, c_0) x Num. Layers * Num. Directions x Batch Size x Hidden Size
        result = torch.zeros(2, 1, batch_size, self.hidden_size)

        if self.use_cuda: return result.cuda()
        else: return result
