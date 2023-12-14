import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from autoencoder.configurations import * 

def get_device():
    if torch.cuda.is_available():
        device = 'cuda:0'
    else:
        device = 'cpu'
    return device

#This is a simple dataset for loading numpy matrices
class NumPy_Dataset(Dataset):
    def __init__(self, embedding_matrix):
        self.embedding_matrix = embedding_matrix

    def __getitem__(self, index):
        return torch.tensor(self.embedding_matrix[index, :]).float()

    def __len__(self):
        return len(self.embedding_matrix)

class AutoEncoder(nn.Module):
    #This model is assumed to be layered
    def __init__(self, input_dimension, hidden_dimensions):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dimension, hidden_dimensions[0]),
            nn.ReLU(True),
            nn.Linear(hidden_dimensions[0], hidden_dimensions[1])
            )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dimensions[1], hidden_dimensions[0]),
            nn.ReLU(True),
            nn.Linear(hidden_dimensions[0], input_dimension)
            )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x
 
    def get_tuple_embedding(self, t1):
        with torch.no_grad():
            return self.encoder(t1).detach().numpy()


class AutoEncoderTrainer:
    def __init__(self, input_dimension, hidden_dimensions):
        super(AutoEncoderTrainer, self).__init__()
        self.input_dimension = input_dimension
        self.hidden_dimensions = hidden_dimensions

    def train(self, embedding_matrix, num_epochs=NUM_EPOCHS, batch_size=BATCH_SIZE):
        self.model = AutoEncoder(self.input_dimension, self.hidden_dimensions)
        self.device = get_device()
        self.model.to(self.device)
        num_tuples = len(embedding_matrix)

        train_dataloader = DataLoader(dataset=NumPy_Dataset(embedding_matrix), batch_size=batch_size, shuffle=True)

        loss_function = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr = LEARNING_RATE)

        self.model.train()

        for epoch in range(num_epochs):
            train_loss = 0
            for batch_idx, data in enumerate(train_dataloader):
                data = data.to(self.device)
                optimizer.zero_grad()
                output = self.model(data)
                loss = loss_function(output, data)
                loss.backward()
                train_loss += loss.item()
                optimizer.step()
            # print('====> Epoch: {} Average loss: {:.4f}'.format(epoch, train_loss / num_tuples))
        
        self.model.eval()
        
        return self.model
    
    def save_model(self, output_file_name):
        torch.save(self.model.state_dict(), output_file_name)

    def load_model(self, input_file_name):
        self.model = AutoEncoder(self.input_dimension, self.hidden_dimensions)
        self.model.load_state_dict(torch.load(input_file_name))
        self.model.eval()
        
