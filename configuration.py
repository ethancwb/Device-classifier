import configparser

config = configparser.ConfigParser()
config.read('config.ini')
Train_loc=config['DEFAULT']['location_Train']
Test_loc=config['DEFAULT']['location_Test']
Model_loc=config['DEFAULT']['model']
train_dataset=config['DEFAULT']['train_dataset']
test_dataset=config['DEFAULT']['test_dataset']

