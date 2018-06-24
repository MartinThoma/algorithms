import matplotlib.pyplot as plt
import numpy as np

csfont = {'fontname': 'Humor Sans'}

with plt.xkcd():
    xs = np.linspace(0, 1, 50)
    plt.plot(xs, (1 / (-xs) + 50) / 50)
    plt.plot(xs, xs, 'r--')
    plt.title('ROC Curve', **csfont)
    plt.xlabel('False Positive Rate', **csfont)
    plt.ylabel('True Positive Rate', **csfont)
    plt.text(0.5, 0.45,
             'Random Classifier',
             horizontalalignment='center',
             verticalalignment='center',
             color='red',
             rotation=36, rotation_mode='anchor')
    plt.text(0.95, 0.8,
             'worse',
             horizontalalignment='center',
             verticalalignment='center',
             color='k',
             rotation=36, rotation_mode='anchor')
    plt.arrow(0.8, 0.8, 0.1, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
    plt.savefig('xkcd-roc-explanation.png')
    # plt.show()
