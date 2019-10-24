build:
	docker build -t prefix-part1:test .

run:
	docker rm -f prefix-part1 || true
	docker run -d --name prefix-part1 -p 6756:6756 prefix-part1:test
