This jenkins job does the clean workspace and git checkout by downloading the git repo, automatically, run the python script (packllist2.py)

pipeline {
    agent {
		node {
			label 'W2K12ENGBLD9'
		}
	}
	
	
	/*parameters {
        //string(name: 'NUGET_PAK', defaultValue: '', description: 'Nuget Package ID')
		//string(name: 'NUGET_Ver', defaultValue: '', description: 'Nuget Package Version')
		//file(name:'', description: 'json list file')
	}*/
	
    stages {
        stage('git repo checkout') {
            steps {
                cleanWs()
                git credentialsId: 'de29ac83ebff-f77dde27-46c2-4049-aee7', url: 'git@github.88-internal.com:Eng-BldAuto/DDS-Signing.git'
            } 
        }
        stage ('Parse python script') {
            steps {
            
                bat "call python packlist2.py" 
            }
        }
    }
}
