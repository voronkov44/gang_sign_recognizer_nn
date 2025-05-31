import numpy as np
import pickle


class NeuralNetwork:
    def __init__(self, input_size, hidden_sizes, output_size):
        self.layer_sizes = [input_size] + hidden_sizes + [output_size]
        self.weights = []
        self.biases = []

        # Инициализация весов и сдвигов
        for i in range(len(self.layer_sizes) - 1):
            scale = np.sqrt(2.0 / (self.layer_sizes[i] + self.layer_sizes[i + 1]))
            self.weights.append(np.random.randn(self.layer_sizes[i], self.layer_sizes[i + 1]) * scale)
            self.biases.append(np.zeros((1, self.layer_sizes[i + 1])))

        self.learning_rate = 0.001
        self.reg_lambda = 0.0001
        self.momentum = 0.9
        self.v_weights = [np.zeros_like(w) for w in self.weights]
        self.v_biases = [np.zeros_like(b) for b in self.biases]
        self.best_weights = None
        self.best_biases = None

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return (x > 0).astype(float)

    def softmax(self, x):
        exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exps / np.sum(exps, axis=1, keepdims=True)

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for i in range(len(self.weights) - 1):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            self.z_values.append(z)
            self.activations.append(self.relu(z))

        z = np.dot(self.activations[-1], self.weights[-1]) + self.biases[-1]
        self.z_values.append(z)
        self.activations.append(self.softmax(z))

        return self.activations[-1]

    def compute_loss(self, y):
        m = y.shape[0]
        probs = self.activations[-1]
        clipped_probs = np.clip(probs, 1e-12, 1.0 - 1e-12)
        correct_log_probs = -np.log(clipped_probs[range(m), y])
        data_loss = np.sum(correct_log_probs) / m
        reg_loss = 0.5 * self.reg_lambda * sum(np.sum(w * w) for w in self.weights)
        return data_loss + reg_loss

    def backward(self, X, y):
        m = y.shape[0]
        grads_w = [np.zeros_like(w) for w in self.weights]
        grads_b = [np.zeros_like(b) for b in self.biases]

        delta = self.activations[-1].copy()
        delta[range(m), y] -= 1
        delta /= m

        grads_w[-1] = np.dot(self.activations[-2].T, delta) + self.reg_lambda * self.weights[-1]
        grads_b[-1] = np.sum(delta, axis=0, keepdims=True)

        for l in range(len(self.weights) - 2, -1, -1):
            delta = np.dot(delta, self.weights[l + 1].T) * self.relu_derivative(self.z_values[l])
            grads_w[l] = np.dot(self.activations[l].T, delta) + self.reg_lambda * self.weights[l]
            grads_b[l] = np.sum(delta, axis=0, keepdims=True)

        for i in range(len(self.weights)):
            self.v_weights[i] = self.momentum * self.v_weights[i] + self.learning_rate * grads_w[i]
            self.v_biases[i] = self.momentum * self.v_biases[i] + self.learning_rate * grads_b[i]
            self.weights[i] -= self.v_weights[i]
            self.biases[i] -= self.v_biases[i]

    def train(self, X, y, epochs=1000, batch_size=64, validation_split=0.2):
        idx = np.random.permutation(X.shape[0])
        split = int(len(idx) * (1 - validation_split))
        X_train, y_train = X[idx[:split]], y[idx[:split]]
        X_val, y_val = X[idx[split:]], y[idx[split:]]

        best_val_acc = 0.0
        no_improve = 0
        patience = 20

        for epoch in range(epochs):
            if epoch % 100 == 0 and epoch > 0:
                self.learning_rate *= 0.9

            idx = np.random.permutation(X_train.shape[0])
            X_train = X_train[idx]
            y_train = y_train[idx]

            epoch_loss = 0
            num_batches = int(np.ceil(X_train.shape[0] / batch_size))

            for i in range(num_batches):
                start = i * batch_size
                end = min(start + batch_size, X_train.shape[0])
                X_batch = X_train[start:end]
                y_batch = y_train[start:end]

                self.forward(X_batch)
                self.backward(X_batch, y_batch)
                batch_loss = self.compute_loss(y_batch)
                epoch_loss += batch_loss

            val_output = self.forward(X_val)
            val_loss = self.compute_loss(y_val)
            val_acc = self.accuracy(X_val, y_val)
            epoch_loss /= num_batches

            if epoch % 10 == 0:
                train_acc = self.accuracy(X_train, y_train)
                print(f"Epoch {epoch}: Train Loss={epoch_loss:.4f}, Val Loss={val_loss:.4f}, "
                      f"Train Acc={train_acc:.2f}%, Val Acc={val_acc:.2f}%")

            if val_acc > best_val_acc + 0.001:
                best_val_acc = val_acc
                no_improve = 0
                self.best_weights = [w.copy() for w in self.weights]
                self.best_biases = [b.copy() for b in self.biases]
            else:
                no_improve += 1
                if no_improve >= patience:
                    print(f"Early stopping at epoch {epoch}. Best val accuracy: {best_val_acc:.2f}%")
                    self.weights = [w.copy() for w in self.best_weights]
                    self.biases = [b.copy() for b in self.best_biases]
                    break

        if self.best_weights is not None:
            self.weights = [w.copy() for w in self.best_weights]
            self.biases = [b.copy() for b in self.best_biases]

        print("Training completed")

    def predict(self, X):
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

    def predict_proba(self, X):
        return self.forward(X)

    def accuracy(self, X, y):
        predictions = self.predict(X)
        return np.mean(predictions == y) * 100

    def save_model(self, filename):
        model_data = {
            'weights': self.weights,
            'biases': self.biases,
            'layer_sizes': self.layer_sizes
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        self.weights = model_data['weights']
        self.biases = model_data['biases']
        self.layer_sizes = model_data['layer_sizes']