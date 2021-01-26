from django.shortcuts import render
from django.http import HttpResponse
from .bset_assoc import BlockSetAssociative

save = [] #holder for download

# Create your views here.
def index(request):
  if request.method == "POST":
    #compute
    if request.POST.get('cache_access_time'):
      global save
      save.clear() 
      t_cache          = int(request.POST.get('cache_access_time'))
      t_mem            = int(request.POST.get('memory_access_time'))
      sets             = int(request.POST.get('sets'))
      n_blocks_per_set = int(request.POST.get('blocks_per_set'))
      words_per_block  = int(request.POST.get('words_per_block'))
      num_list         = request.POST.get('input').splitlines()
      num_list         = [int(i) for i in num_list] #convert all to int
      iterations       = int(request.POST.get('iteration'))
      bs = BlockSetAssociative(
        n_sets=sets, 
        n_blocks=n_blocks_per_set, 
        num_list=num_list, 
        n_words=words_per_block,
        t_cache=t_cache,
        t_mem=t_mem,
        debug=False)
      #TODO: convert to print on screen, add error checking
      for i in range(iterations):
        print(f'\n\nIteration: {i}')
        if(i != 0):
          save.append('\n\n')
        save.append(f'Iteration: {i}'+'\n')
        bs.lru()
        save.append(bs.print_cache())
        save.append(bs.print_stats())
        bs.hits = 0
        bs.misses = 0
    #download
    else: 
      file_data = save
      response = HttpResponse(file_data, content_type='application/text charset=utf-8')
      response['Content-Disposition'] = 'attachment; filename="BSA_LRU_answer.txt"'
      return response
  return render(request, 'pages/home.html')