Classifier:

First we need to run the pcap file parser in order to get the field we want:

    Parser_for_insteon_hub.py:
        Take in a main path and goes into every sub-directory and loop through all the pcap files.
        For example, take in "unctrl/", it will loop through every sub-directory(each sub-directory is a device) inside unctrl folder.
        The script will generate 7 csv files for each device. And it will not stop until it finishes all the devices inside the main
        directory. Ideally 7 * device_count files will be generated in the end, unless some devices doesn't have enough data to generate the csv.
        7 files are: 
            1. dns_features.csv, this csv includes all the dns fields we need to further extract features.
            2. dstport.csv, this csv includes all the fields we need to further extract destination port(udp & tcp) related feature.
            3. general.csv, this file includes all the field we need to further extract protocol features.
            4. http.csv, this files includes all the field we need to further extract http features.
            5. payload.csv, this csv includes all the fields we need to further extract payload_size features.
        And it will also generate 2 more files for testing purpose, since we currently don't have enough test data. But they could be deleted in the end.
        
        As documented in the file, it contains 5 parts responding to the 5 main csv files it is generating.
 
 
 After that, we need to run the feature extractor to extract the features we need to pass into the machine learning model:
    
    dns_data_processor.py:
        This file contains the feature extractor for the 5 main files. The file take 5 files(dns, http, general, dstport, payload) as input, will return the
        extracted feature dictionary in the end. Each time we run the file, it will finish the feature extraction for one device. This file is being looped again
        and again by the main classifier file in order to get all the extracted features for all devices. 
        
        Although we've commented out some of the old feature, the features we are currently using are:
            eth.src_resolved
            cname
            qname
            rname
            http_host
            http_server
            protocol
            dstport
            payload_size
            time_delta
        We modified this file whenever we need some new features in the final training model.
        
    classifier:
    It internally call the dns_data_processor.py file to extract the features and create the train and test data.
    machine learning algorithm can be be chosen based on the training or testing performed.
    The supported ML algorithms are Decision Tree,Logistic Regression and Support vector machine.
    It is a multiclass classifier which predict the MAC address of the device.
    Saves the model generated as well as the feature list as a pickle file
    
    predictoion.py.
    Loads the features pickle file and generates  test data where as choice of model can be picked based on the machine learning chosed
     
    config.ini
    takes in the parameters such as location of training,testing data and also where the models and the features list has to be stored
    
    configuration.py
    pareses the config.ini file and passes as arguments to the classifeir and the prediction
    
    Spertare