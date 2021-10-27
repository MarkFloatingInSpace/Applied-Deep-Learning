# "TrackMania 2020" Bot Using a Combination of Supervised Regression and Reinforcement Learning in a Deep CNN

TrackMania 2020 is a free-to-play racing game video game where players compete on different tracks to obtain the fastet times. A map editor is available for subscription-paying users. 

The goal of this project is to build and train a deep convolutional neural network in order to drive on specially created maps. The project is done in the context of the "Applied Deep Learning" university course of TU Wien, falling under the "Bring your own Method" type of project within the course.

The environment for the reinforcement learning as well as the data source of the supervised learning will be custom generated maps originateing from the map editor of the game. Official TrackMania 2020 maps exhibit extrem complexity and a wide variety of track features including loops, different surfaces, water, banked turns, flying, driving on the ceiling, boost, no-engine segments and multiple finish options. This  leads to poor generalizability between tracks. Furthermore, the course of the track is often unclear even for human players, requiring familarity with the individual track in order to perform well or even finishing at all. Therefore the scope of this project is limited to custom created tracks exhibiting similar features among themselves with a limit selection of track features.

The data for the supervised training will be collected using five human drivers and the built in replay functionality of the game. The obtained replays conventiently also include the control input of the players. The feature-target pairs will consist of (cropped, downscaled, grey-scale) images of the player's screen and the control input. The control input consists of three continous number specifing the steering, accelerator and break inputs.

The training is planed to be done in two stages. First, supervised learning using replays of runs is employed to tune hyperparameters, especially the network architecture, and pretrain the model. Subsequently reinforcement learning is used to improve the model.

Evaluation of the model performance is planed to be done using human performance both on the tracks used for training the model as well as on unseen tracks. The expected time of the model is 30% slower for tracks that are part of the training set and 50% slower on the unseen tracks.

Tasks
1.	Build maps using the map editor of TrackMania 2020. 5 h
1.	Gather replays of players playing the custom maps; 3 h
1.	Preprocess data: Rendering replays, frame extraction, downscaling,..., 10 h
1.	Generate training and test data sets using the preprocessed data 2 h
1.	Create a simple first model and train it in a supervised fashion 15 h
1.	Tune model architecture, employing hyper-parameter tuning using cross-validation, etc.; 30 h
1.	Save pretrained CNN after tuning 1 h
1.	Implement reinforcement learning for specific envionment 15 h
1.	Imporve reward function 10 h
1.	Train pretrained model; 1 week of unsupervised time
1.	Evaluating, Plotting, Analysing results 10 h
1.	Report 15 h
1.	Presentation 15 h

Relevant Scientific Papers:
*  Anderson, Charles W. et al. “Faster reinforcement learning after pretraining deep networks to predict state dynamics.” 2015 International Joint Conference on Neural Networks (IJCNN) (2015): 1-7.
*  Kaelbling, Leslie Pack, Michael L. Littman, and Andrew W. Moore. "Reinforcement learning: A survey." Journal of artificial intelligence research 4 (1996): 237-285.
