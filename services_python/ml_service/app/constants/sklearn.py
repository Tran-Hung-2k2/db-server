SKLEARN_CONFIG = [
    {
        "task": "Classification",
        "models": [
            {"code": "linear_model", "name": "LogisticRegression"},
            {"code": "svm", "name": "SVC"},
            {"code": "neighbors", "name": "KNeighborsClassifier"},
            {"code": "tree", "name": "DecisionTreeClassifier"},
            {"code": "ensemble", "name": "RandomForestClassifier"},
            {"code": "naive_bayes", "name": "GaussianNB"},
            {"code": "ensemble", "name": "GradientBoostingClassifier"},
        ],
        "metric": [
            {"code": "accuracy_score", "name": "Accuracy Score"},
            {"code": "precision_score", "name": "Precision Score"},
            {"code": "recall_score", "name": "Recall Score"},
            {"code": "f1_score", "name": "F1 Score"},
            {"code": "roc_auc_score", "name": "ROC AUC Score"},
            {"code": "confusion_matrix", "name": "Confusion Matrix"},
        ],
        "datasets": [
            {
                "code": "load_iris",
                "name": "Iris Dataset",
                "description": "This dataset contains measurements of iris flowers, with three classes of iris species",
            },
            {
                "code": "load_breast_cancer",
                "name": "Breast Cancer Dataset",
                "description": "This dataset contains breast cancer diagnostic data",
            },
            {
                "code": "load_digits",
                "name": "Digits Dataset",
                "description": "This dataset consists of 8x8 pixel images of handwritten digits",
            },
        ],
    },
    {
        "task": "Regression",
        "models": [
            {"code": "linear_model", "name": "LinearRegression"},
            {"code": "linear_model", "name": "Ridge"},
            {"code": "linear_model", "name": "Lasso"},
            {"code": "tree", "name": "DecisionTreeRegressor"},
            {"code": "ensemble", "name": "RandomForestRegressor"},
            {"code": "ensemble", "name": "GradientBoostingRegressor"},
        ],
        "metric": [
            {"code": "mean_absolute_error", "name": "Mean Absolute Error"},
            {"code": "mean_squared_error", "name": "Mean Squared Error"},
            {"code": "r2_score", "name": "R-squared Score"},
        ],
        "datasets": [
            {
                "code": "load_boston",
                "name": "Boston Housing Dataset",
                "description": "This dataset contains information collected by the U.S. Census Service concerning housing in the area of Boston Mass.",
            },
            {
                "code": "load_diabetes",
                "name": "Diabetes Dataset",
                "description": "This dataset contains ten baseline variables, age, sex, BMI, average blood pressure, and six blood serum measurements, for 442 diabetes patients",
            },
        ],
    },
    {
        "task": "Clustering",
        "models": [
            {"code": "cluster", "name": "KMeans"},
            {"code": "cluster", "name": "DBSCAN"},
            {"code": "cluster", "name": "AgglomerativeClustering"},
        ],
        "metric": [
            {"code": "silhouette_score", "name": "Silhouette Score"},
            {"code": "davies_bouldin_score", "name": "Davies-Bouldin Score"},
        ],
        "datasets": [
            {
                "code": "load_iris",
                "name": "Iris Dataset",
                "description": "This dataset contains measurements of iris flowers, with three classes of iris species",
            },
            {
                "code": "load_digits",
                "name": "Digits Dataset",
                "description": "This dataset consists of 8x8 pixel images of handwritten digits",
            },
        ],
    },
    {
        "task": "Dimensionality Reduction",
        "models": [
            {"code": "decomposition", "name": "PCA"},
            {"code": "decomposition", "name": "TruncatedSVD"},
        ],
        "metric": [
            {"code": "explained_variance_score", "name": "Explained Variance Score"},
            {"code": "mean_squared_error", "name": "Mean Squared Error"},
        ],
        "datasets": [
            {
                "code": "load_digits",
                "name": "Digits Dataset",
                "description": "This dataset consists of 8x8 pixel images of handwritten digits",
            }
        ],
    },
    {
        "task": "Ensemble Methods",
        "models": [
            {"code": "ensemble", "name": "VotingClassifier"},
            {"code": "ensemble", "name": "VotingRegressor"},
            {"code": "ensemble", "name": "BaggingClassifier"},
            {"code": "ensemble", "name": "AdaBoostClassifier"},
            {"code": "ensemble", "name": "GradientBoostingClassifier"},
        ],
        "metric": [
            {"code": "accuracy_score", "name": "Accuracy Score"},
            {"code": "roc_auc_score", "name": "ROC AUC Score"},
        ],
        "datasets": [
            {
                "code": "load_iris",
                "name": "Iris Dataset",
                "description": "This dataset contains measurements of iris flowers, with three classes of iris species",
            },
            {
                "code": "load_breast_cancer",
                "name": "Breast Cancer Dataset",
                "description": "This dataset contains breast cancer diagnostic data",
            },
        ],
    },
]
