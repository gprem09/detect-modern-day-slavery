import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tqdm import tqdm

class NeuralNetworkTrainer:
    def __init__(self, data_path, model_path='mlp_model.h5', epochs=100, batch_size=32):
        self.data_path = data_path
        self.model_path = model_path
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
    
    def load_data(self):
        """Load the dataset and return coordinates (latitude, longitude)."""
        try:
            df = pd.read_csv(self.data_path)
            df['latitude'] = df['latitude'].astype(float)
            df['longitude'] = df['longitude'].astype(float)
            coordinates = df[['latitude', 'longitude']].values
            print(f"Data loaded successfully. {len(coordinates)} points found.")
            return coordinates
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def generate_synthetic_legal_points(self, coordinates, num_points=100):
        """Generate synthetic legal points within the bounds of illegal points."""
        min_lat, max_lat = coordinates[:, 0].min(), coordinates[:, 0].max()
        min_lon, max_lon = coordinates[:, 1].min(), coordinates[:, 1].max()

        synthetic_latitudes = np.random.uniform(min_lat, max_lat, num_points)
        synthetic_longitudes = np.random.uniform(min_lon, max_lon, num_points)

        legal_points = np.column_stack((synthetic_latitudes, synthetic_longitudes))
        print(f"Generated {num_points} synthetic legal points.")
        return legal_points

    def build_model(self):
        """Build a simple Neural Network."""
        model = Sequential()
        model.add(Dense(32, input_dim=2, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model
        print("Neural Network model built.")
    
    def train(self, illegal_points, legal_points):
        """Train the neural network with illegal and legal points."""
        illegal_labels = np.ones(len(illegal_points))
        legal_labels = np.zeros(len(legal_points))

        X = np.vstack((illegal_points, legal_points))
        y = np.hstack((illegal_labels, legal_labels))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.build_model()

        for epoch in tqdm(range(self.epochs), desc="Training Progress", ncols=100):
            history = self.model.fit(X_train, y_train, epochs=1, batch_size=self.batch_size, verbose=0, validation_data=(X_test, y_test))

            train_acc = history.history['accuracy'][0]
            val_acc = history.history['val_accuracy'][0]
            print(f"Epoch {epoch+1}/{self.epochs}: Training accuracy: {train_acc:.4f}, Validation accuracy: {val_acc:.4f}")
        
        self.model.save(self.model_path)
        print(f"Model saved as {self.model_path}.")

if __name__ == "__main__":
    data_path = 'static/dataset/illegal_deforestation.csv'
    model_path = 'mlp_model.h5'
    epochs = 100
    batch_size = 32

    trainer = NeuralNetworkTrainer(data_path, model_path, epochs, batch_size)
    illegal_points = trainer.load_data()

    if illegal_points is not None:
        legal_points = trainer.generate_synthetic_legal_points(illegal_points, num_points=100)

        trainer.train(illegal_points, legal_points)
    else:
        print("Failed to load data.")
