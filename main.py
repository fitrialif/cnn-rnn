import argparse
import os
from urllib.request import urlretrieve
from zipfile import ZipFile
from dataset.dataset import Dataset
from network.train import Network

parser = argparse.ArgumentParser()
parser.add_argument("-esize", type=int, dest='size', help="Size of examples ")
parser.add_argument("-estep", type=int, dest='step', help="Size of step for grouping frames into examples")
parser.add_argument("-height", type=int, dest='height', help="Height of frames")
parser.add_argument("-width", type=int, dest='width', help="Width of frames")
parser.add_argument("-lrate", type=float, dest='lrate', help="Learning rate")
parser.add_argument("-cnn", type=str, dest='cnn', help="usual/inception cnn block")


parser.add_argument("-u", "--update", action='store_true', help="Re-create tfrecords")
parser.add_argument("-d", "--download", action='store_true', help="Download dataset")
parser.add_argument("-r", "--restore", action='store_true', help="Re-store checkpoint")
parser.add_argument("-is_training", action='store_true', help="Is test?")

dataset_urls = [
    "http://cvrc.ece.utexas.edu/SDHA2010/videos/competition_1/ut-interaction_segmented_set1.zip",
    "http://cvrc.ece.utexas.edu/SDHA2010/videos/competition_1/ut-interaction_segmented_set2.zip"]

tmp_zip_adr = os.path.join(os.getcwd(), 'dataset/data/tmp.zip')
data_dir = os.path.join('dataset/data/')
logs_path = 'network/logs'


def run():
    download_dataset_if_needed()
    if args.update:
        print("Starting processing binary dataset")
        Dataset(args).create_dataset(data_dir + "segmented_set?/*.avi")
    if args.is_training is True:
        print("Begin training")
        Network(args).begin_training()
    else:
        print("Begin test")
        Network(args).begin_test()

def download_and_unzip(zipurls):
    for url in zipurls:
        print("Downloading {}".format(url))
        fpath, _ = urlretrieve(url, tmp_zip_adr)

        zf = ZipFile(fpath)
        zf.extractall(data_dir)
        zf.close()
        os.remove(fpath)
    print("Dataset downloaded into 'dataset/data' folder")


def download_dataset_if_needed():
    if not os.path.exists(data_dir) or args.download:
        os.makedirs(data_dir)
        print("Downloading dataset")
        download_and_unzip(dataset_urls)


if __name__ == '__main__':
    args = parser.parse_args()
    run()
