from django.shortcuts import render

from algorithms.forms import Form
from algorithms.models import Algorithm

from algorithms.inputHandling import csvInput, cleanUp, randomArray
from io import TextIOWrapper
import copy
from algorithms.choiceAlgorithms import *


# define available alogithms names
algorithmNames = ['Bubble sort', 'Insert sort', 'Merge sort', 'Count sort',
'Quick sort', 'Linear search', 'Binary search', 'Binary tree search']
# define available algorithm functions
algorithms = [bubble, insert, merge, counting, quickSort, linearSearch,
binarySearch, Tree.binarySearch]

# show all algorithms on the index page
def algorithms_index(request):
    algorithms = Algorithm.objects.all()
    context = {"algorithms": algorithms}
    return render(request, "algorithms_index.html", context)

# show all algorithms that have the category selected
def algorithms_category(request, category):
    algorithms = Algorithm.objects.filter(categories__name__contains=category)
    context = {"category": category, "algorithms": algorithms}
    return render(request, "algorithms_category.html", context)

# show the algorithm with all its properties and provide input form
def algorithms_detail(request, pk):
    algorithm = Algorithm.objects.get(pk=pk)
    if request.method == "POST":
        form = Form(request.POST)
        # case: user choice
        if request.POST['choice'] == 'csv':
            if 'file' in request.POST:
                dataInput='No csv file selected'
            else:
                try:
                    # if it's a csv file, decode the binary file into a text encoding
                    f = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
                    dataInput = csvInput(f)
                except:
                    dataInput = 'Invalid csv file selected. Could not decode.'
        elif request.POST['choice'] == 'own':
            if request.POST['description'] == '':
                dataInput = 'Empty input'
            else:
                # use regular expressions to clean up user array input
                dataInput = cleanUp(request.POST['description'])
                if not dataInput:
                    dataInput = "Input array contains non-numbers"
                elif algorithm.title == 'Binary search':
                    if dataInput != sorted(dataInput):
                        dataInput = "Provided list is not sorted (binary search doesn't on unsorted lists)"
                elif algorithm.title == 'Binary tree search':
                    dataInput.sort()
        elif request.POST['choice'] == 'random':
            if request.POST['description'] == '':
                dataInput = 'Empty input'
            else:
                # generate random array with user defined parameter
                dataInput = randomArray(request.POST['description'])
                if not dataInput:
                    dataInput = "Invalid syntax; syntax: start, end, number of entries, e.g. -5, 5, 7"
                elif algorithm.title in ('Binary search', 'Binary tree search'):
                    dataInput.sort()
        context = {'algorithm': algorithm}
        if algorithm.purpose == 'Search':
            # if it's a search algorithm, get the target element too
            context['target'] = request.POST['target']
            try:
                context['target'] = int(context['target'])
            except:
                dataInput = 'Target is not an integer'
        # change context and run different view depending on whether an error occured
        if type(dataInput)==str:
            context['error'] = dataInput
            return algorithms_error(request, context)
        else:
            context['data'] = dataInput
            return algorithms_result(request, context)
    else:
        form = Form()
    context = {"algorithm": algorithm, 'form':form}
    return render(request, "algorithms_detail.html", context)

# show error message that occured
def algorithms_error(request, context):
    return render(request, 'algorithms_error.html', context)

# display the result of the algorithm
def algorithms_result(request, context):
    # find and select the algorithm to use
    position = algorithmNames.index(context['algorithm'].title)
    data = copy.deepcopy(context['data'])

    if context['algorithm'].purpose == 'Search':
        if context['algorithm'].title == 'Binary tree search':
            # it it's a binary tree, crete tree first
            tree = Tree(data)
            time, numOps, index, arrayPositions = timeAlgorithm(tree.binarySearch, data, context['target'], tree.rootNode)
        else:
            time, numOps, index, arrayPositions = timeAlgorithm(algorithms[position], data, context['target'])
        # add the results to the context dictionary
        context['position'] = index
        context['sorted'] = ''
    else:
        time, numOps, sortedData, arrayPositions = timeAlgorithm(algorithms[position], data)
        # add the results to the context dictionary
        context['position'] = 'NaN'
        context['sorted'] = sortedData
    # add some data to context dictionary
    context['time'] = time
    context['numOps'] = numOps
    context['arrayPositions'] = arrayPositions
    context['indexes'] = list(range(len(context['data'])))
    return render(request, 'algorithms_result.html', context)
