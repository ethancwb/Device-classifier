Config.ini:
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
location_Train: The location of all the pcap files for training.
location_Test: the location of all the pcap files for testing.
Model: The location of pre-trained model, if any
Classses: Multiclass / single-class
Train_dataset: The location of training csv, generated from all the training pcap files
Test_dataset: The location of testing csv, generated from all testing pcap files
Parameter: Whether we need to generate a new training / testing csv.
Pcap_location: The location of all raw pcap files.
Output_location: The output location of all parsed csvs.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

First we need to run the pcap file parser in order to get the fields we want:

Rawdataparser.py:
Set up the correct “pcap_locaiton” as well as “output_location” in “config.ini”. Then run it with: “python Rawdataparser.py”. The “pcap_location” should be the absolute path to root directory of where the stored pcap files are.
For example, take in "unctrl/", it will loop through every sub-directory (each sub-directory should contains sufficient pcap files for training and testing of a particular device) inside unctrl folder.
The script will generate 10 different csv files for each device (5 for training, 5 for testing). It will not stop until it finishes all the devices inside the main directory. Ideally 8 * device_count files will be generated in the end, unless some devices doesn't have enough data to generate the csv.
10 files are:
1. dns_features.csv, this csv includes all the dns fields we need to further extract features.
2. dstport.csv, this csv includes all the fields we need to further extract destination port(udp & tcp) related feature.
3. general.csv, this file includes all the field we need to further extract protocol features.
4. http.csv, this files includes all the field we need to further extract http features.
5. payload.csv, this csv includes all the fields we need to further extract payload_size features.
It will also generate 5 more files for testing purpose. This is done be automatically taking the most recent pcap file for each device as the testing dataset..

As documented in the file, it contains 5 parts responding to the 5 main csv files it is generating. For data sanitizing, there is also an optional “shrink_output_size” method, which keep every output csv has a same data size.



feature_processor.py:
This file contains the feature extractor for the csvs files. The file take 5 files(dns, http, general, dstport, payload) as input, will return the extracted feature dictionary in the end. Each time we run the file, it will finish the feature extraction for one device. This file is being looped again and again by the main classifier file in order to get all the extracted features for all devices. Thus, we do not need to run it manually.

Although we've commented out some of the old feature, the features we are currently using are:
eth.src_resolved
cname
qname
rname
http_host
protocol
dstport
payload_size
time_delta

Classifier.py:
Set up the “location_Train” and “Train_dataset” in the config.ini file. “location_Train” is the location of all the training csvs, generated by raw_data_parser.py. “Train_dataset” is the location of “train.csv”, which is the output of “Classifier.py”. Then setup the path to “model” in the config.ini file if you want to use a pre-configured model. At last, set “Parameter” to be false if there is no change in training dataset, set “Parameter” to be true if a new dataset needs to be generated.
Run by command: “python classifier.py”

This file internally call the feature_processor.py file to extract the features and create the train and test dataset for creating a machine learning model. Different machine learning algorithm can be be chosen based on the training or testing performed. The supported ML algorithms are Decision Tree, Logistic Regression, Support vector machine, Random Forest. It is a multiclass classifier which predict the MAC address of the device. In order to save time for following training & testing, it will generate one “training.csv” file that contains all the extracted features of current dataset. If there is nothing changed in the training pcap files, we can set the “parameter” in the config.ini to be false and thus the classifier will not extract features again and directly use the “training.csv” file to train the new model. This is extremely useful when we want to test will different algorithms or change the configuration of algorithms.

Prediction.py:
Setup the “location_Test” and “Test_dataset” in the config.ini. “location_Test” is the location of all the testing csvs, generated by raw_data_parser.py. “Test_dataset” is the location of “test.csv”, which is the output of “Prediction.py”. Similar with “classifier.py”, “prediciton.py” transfer all testing csvs into one single “test.csv” and then feed the test features to the machine learning model made by “classifier.py” to predict the results. This file is run by “python prediction.py”. Again, for simplicity, it will generate one “test.csv” file that contains all the extracted features of current testing dataset. If there is nothing changed in the testing pcap files, we can set the “parameter” in the config.ini to be false and thus the predictor will not extract features again and directly use the “test.csv” file to predict. This is extremely useful when we want to test will different algorithms or change the configuration of algorithms.

Configuration.py:
pareses the config.ini file and passes as arguments to the classifier and the prediction files.



Work flow:
1, run the rawdataparser.py to parse the pcap file of all devices. This will generate 9 csv files as output for each device.
2, put all the training data in a folder, and all test data in a folder. Then put all the path configuration to the config.ini.
3, run the classifier.py and set the parameter to false. That will generate a new model and a training.csv.
4, run the predict.py and set the parameter to false. That will apply the model on the test files and generate the accuracy.

