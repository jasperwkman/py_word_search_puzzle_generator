d:
cd D:\projects\py_world_search_puzzle_script
#all env\Scripts\activate
$start = 7
$end = 7
$j = 1
for ($i = $start; $i -le $end; $i++)
{
    python app.py $i regen_words
    for ($j = 1; $j -le 5; $j++)
    {
        python app.py $i $j
    }
}

for ($i = $start; $i -le $end; $i++)
{
        python .\make_solution_page.py $i
}