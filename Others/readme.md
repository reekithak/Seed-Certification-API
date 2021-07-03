## ATTEMPT & GENERAL USE:
The project focuses on problem of certifying seeds manually before distributing them
to farmers. Usually done by govt agencies, which is costly and contains a lot of manual labour.
The project is based on 3 different Deep Learning Models that asses 3 different features of seeds respectively. [ Color, Crack, General Quality ]

## MODULES:
1)	3 individual ML-Models combined to form a single API. ( Web App )
2)	ReactJs Based Frontend UI. (Static Web App)
Hosted both separately into Azure Cloud Services

## FOCUS:
Compared to traditional methods, this is cheap & has less manual work. The project focuses on capturing real-time pictures of the seeds and sends it to the API for evaluation.
The API returns a json output of the test scores which is further processed by the react app for proper output.
The Architecture of the Models are based on Modified RESNETs.

## MY ROLE (Akhil):
Developed the complete Backend part which includes:
1)	Training Models
2)	Testing and Combining the API’s
3)	Deploying the API to cloud service
The Backend is based on python and uses FLASK Server.

## TOOLS & TECH:
1)	Languages: Python, JavaScript.
2)	Platform/OS: Windows.
3)	Server/Backend: Flask.
4)	Models: TensorFlow, Keras, Scikit-Learn.
5)	Frontend/UI: ReactJS.
6)	Workspace: Jupyter Notebooks, VSCode.

## CHALLENGES:
The main challenge was with training the models & attaining the right quality for each of them. We were on deadline for a competition.
So didn’t have the luxury to train all of them one by one. Even Colab used to get disconnected.
So Took 3 RDP’s & Trained each Model Separately.

## MEMBERS:
There were 4 people. 2 of us for the implementation, the other two for the documentation & other official purposes.

## TIME TAKEN:
4 total days to develop and deploy the API. 2 days for the frontend & 1 day for the integration. So Total 7 days for the entire project.

## FUTURE AND FURTHER DEVELOPMENTS:
1)	Planning to implement a Raspberry PI Based system to detect Germination. We’re planning to add 2 more members to the team for electronics & hardware part, while we deal with the software. 
2)	Trying to improve the model quality

## DRAWBACKS:
Lack of sufficient Data & less computation Power. In short shortage of adequate resources.
