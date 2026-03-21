import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from matplotlib.widgets import Button

# Generate synthetic dataset
np.random.seed(0)
X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
y = [0] * 20 + [1] * 20

# Train initial SVM model
model = SVC(kernel='linear')
model.fit(X, y)

# Set up plot
fig, ax = plt.subplots(figsize=(8, 6))
scatter = None


def plot_decision_boundary():
    global scatter
    ax.clear()
    # Plot points
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolors='k')

    # Create meshgrid
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 500),
                         np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 500))
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot decision boundary and margins
    ax.contour(xx, yy, Z, colors='k', levels=[0], linestyles=['-'])
    ax.contourf(xx, yy, Z > 0, alpha=0.2, cmap='coolwarm')
    ax.set_title("Interactive SVM Decision Boundary")


# Mouse click event
def onclick(event):
    global X, y, model
    if event.inaxes != ax:
        return
    # Left click = Class 0, Right click = Class 1
    label = 0 if event.button == 1 else 1
    new_point = np.array([[event.xdata, event.ydata]])
    X = np.vstack([X, new_point])
    y.append(label)

    # Retrain model
    model.fit(X, y)
    plot_decision_boundary()
    plt.draw()


# Reset button
def reset(event):
    global X, y, model
    np.random.seed(0)
    X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
    y.clear()
    y.extend([0] * 20 + [1] * 20)
    model.fit(X, y)
    plot_decision_boundary()
    plt.draw()


# Plot initial decision boundary
plot_decision_boundary()

# Add reset button
reset_ax = plt.axes([0.8, 0.01, 0.1, 0.05])
button = Button(reset_ax, 'Reset', color='lightblue', hovercolor='skyblue')
button.on_clicked(reset)

# Connect click event
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()