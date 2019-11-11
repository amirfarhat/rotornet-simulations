
# run variables
capacity=1
tors=10
rotors=1

# set up results file
results_dir=results
mkdir -p $results_dir
eval results_file="$results_dir/run-$tors-$rotors-$capacity.txt"
touch $results_file

for i in {1..100}
do
	echo "Run $i"
	python3 main.py -c $capacity -t $tors -r $rotors --results_file $results_file
done