from wordcloud import WordCloud
import pandas as pd
from wordcloud import STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image
from pathlib import Path
import json


def create_wordcloud(csv_path: Path, column: str, output_file: Path):
    df = pd.read_csv(csv_path)

    data = "\n".join([str(el) for el in df[column].tolist()])

    be_mask = np.array(Image.open("python-logo.png"))
    h, w, d = be_mask.shape

    STOPWORDS.update({"None", "nan", "Python", "python3"})
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        width=1920,
        height=1080,
        background_color="white",
        mask=be_mask,
    ).generate(data)

    image_colors = ImageColorGenerator(be_mask)

    import matplotlib.pyplot

    wc = wordcloud
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    fig = matplotlib.pyplot.gcf()
    dpi = 100
    tight_correction = 1.29
    fig.set_size_inches(1920 / dpi * tight_correction, 1080 / dpi * tight_correction)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    ax1.axis("off")
    fig.savefig(output_file, bbox_inches="tight", dpi=dpi)


if __name__ == "__main__":
    with open("secret.json") as fp:
        secrets = json.load(fp)
    create_wordcloud(
        f"{secrets['meta_folder']}/pypi-packages.csv",
        "keywords",
        f"{secrets['meta_folder']}/wordcloud-keywords.png",
    )
    create_wordcloud(
        f"{secrets['meta_folder']}/pypi-packages.csv",
        "summary",
        f"{secrets['meta_folder']}/wordcloud-summary.png",
    )
