AMPLab Arab-Andalusian

LINUX PYTHON TEMPLATE PROJECT

Run from root directory: 
	docker-compose run -p 8080:8080 ubuntu

Or run from the root directory:
	docker image build -t <name>:<tag> <directory_of_the_dockerfile>
	docker run -v $(pwd):/data/ -p 8080:8080 -it <name>:<tag> bash

write dependancies in:
	 ./docker_image/requirements.txt
	 (this requires the image to be rebuilt)

once in the linux terminal run:
	jupyter lab --port=8080 --ip=0.0.0.0 --allow-root
	jupyter notebook --allow-root --ip=0.0.0.0 --port=8080
to start jupyterAMPLab Arab-Andalusian Paper