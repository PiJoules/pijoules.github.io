Title: Technical Interview Notes
Date: 2016-07-12 13:34
Category: Notes
Tags: Algorithm, Sorting, Data Structure, Technical, Interview
Authors: Leonard Chan

## Sorting

- **Divide and conquer**: Splitting a problem into smaller problems similar to the initial until a point is reached where the problem is small enough that it can be solved on its own. Aftwerards, the solution is propogated back up to help solve the higher problem.
- **Inplace**: Elements in the array are swapped when sorted instead of having a new sorted array returned.


### Merge Sort
Divide and conquer sorting algorithm that sorts by splitting up an array into smaller chunks to be sorted. The chunks are split halfway until they are each of size 1. In this case, the chunks are already sorted. After dividing, pairs of sorted arrays are joined together, sorting them as they are merged until there is only one chunk left that is the final sorted array.

- Best, average, and worst case time complexities are all O(nlog(n)). The complexity of the merging step is O(nlog(n)) since each merge involves iterating through both chunks in each pair, which grows with the length of the original array (n) and the number of merges decreases by a factor of 2 since half the number of chunks to merge remain after each process of merging.
- The space complexity is O(n) since the sorted elements need to be stored in some intermediary when merging. This number increases based on the length of the initial array. As a result, the algorithm is also not inplace.

### Quicksort
Divide and conquer algorithm that sorts very similarly to merge sort, but uses a pivot and wall to swap elements in place, avoiding having to create temporary arrays when merging. Quicksort works by partitioning the array into two partitions based on a pivot such that everything to the left of the pivot is less than it, and everything to the right of the pivot is greater than it. The new position of the pivot after the partitioning is kept track of by an incrementing wall/counter for the start of the array. The pivot itself is an arbitrary element in the array.

The partitioning works by iterating through all the elements of the array, swapping elements that are less than the pivot with the element immmediately to the left of the wall (which starts at index 0). Aftwerwards the wall inc incremented by 1, moving the wall to the right of the newly formed partition. After iterating through all elements, the pivot is swapped with the current element at the wall. At this point, the array is divided into 3 sections: the left partion of elements less than the pivot, the pivot itself, and the right partion of elements greater than (or equal to) the pivot.

The algorithm continues by applying this partitioning and sorting on the newly formed left and right partitions until the partions are of size 1, in which case, they are sorted. After having gone through all sub-partitions, the entire array has been sorted inplace.

- The main action done in this algorithm behind the sorting is the swapping of elements, which has a constant space and time complexity since swapping just involves having a single temporary variable.
- The wort case time complexity is $O(n^2)$ where the partitions are very imbalanced, causing either the left or right partion to always be of size 0. In this case, the division step creates a new partition whose length is just 1 less the previous which must still be iterated over to produce another partition. Both the iteration in each partition, and the number of partitions made increase with the length of the array, n. This scenario occurs in the case where either the smallest or largest elements in the array are chosen as the pivot for all partions since all other elements must be to the left of the partition if the max is chosen and to the right of the partition if the min is always chosen. To make sure the min and max aren't always selected, the median of the first handful of elements in the array is used as the pivot.
- The average and best case time complexities are both O(nlog(n)). For best case, this occurs if the sub-partitions created are of equal size since the size of each sub partiion decreases by a factor of 2 each time. Always happenning to select the median of the partition can lead to this. The average case involves complex math, so see [Khan Academy](https://www.khanacademy.org/computing/computer-science/algorithms/quick-sort/a/analysis-of-quicksort) for a better explanation.
- The space compelxity is constant since the array is sorted inplace and all the swaps just use 1 temporary variable.


## Hash Tables
Hash tables (also known as dictionaries, maps, associative arrays) are abstract data types where each value is associated with a unique key. The elements themselves are actually stored in an array. The element index/offset at which these elements are stored is the result of a hash function for a given key. This hash function is responsible for converting a given data type to an integer representation of it for this offset.

### Hash Function
The hash function itself should be implemented in such a way that the hash for a variable can be calculated quickly (near constant time), and each hash produced should be unique for every unique key. As a result, most of the time, hash functions involve some complicated math involving prime numbers, and coming up with a universal hash function that works for nearly all data types is impossible. (See [python's implementation for string hashing](https://github.com/python/cpython/blob/2.7/Objects/stringobject.c) as an example of how hashing works. I tend to use python's hashing functions when implementing my own hash tables.) If a hash function produces a hash whose value is at least the length of the array, the hash hash is modulo'd with the length of the array to produce an index that can be used on this array.

### Collisions
Regardless of how well the hashing algorithm is, there is a possibility that two keys could produce the same hash, in which case, if an element already occupies the space for that hash, the element will still have to be stored somehow (it should not be dropped.) 

In the event collisions occur, the hash function should be able to produce a uniform distribution of hashes, allowing for all elements to be accessed in an equal amount of time. A bad hash function produces a distribution of hashes such that a majority of the resulting hashes are the same or close to each other, resuliting in a distribution with peaks. If the hashes produced for a wide range of keys is the same, lookup is similar to lookup in a list.

Two ways to handle keys with duplicate hashes are through separate chaining and open addressing:

- Separate chaining involves having each element in the hash table be a list (typically a linked list), and just appending an element at this hash to the linked list. This way, values for keys with duplicate hashes can still be stored at these hashes.
- Open addressing involves placing values in the next available empty space in the array. If the space for a given hash is already occupied, the next available space is selected according to some probe sequence which returns the next hash to use for a given hash. Common ones include linear probing which just increments the hash by 1 until an empty space is found. Quadratic probing involves incrementing the hash by the square of the kth iteration into the probing function.

Both operations involve iterating over some sequence when collisions occur, effectively scaling up lookup linearly. In order to prevent collisions, some hash table implementations will dynamically resize the array to allow for more hashes to be stored. This assumes that the collisions are primarly a result of modulo-ing against the length of the array and not a result of the distribution of hashes formed by the funciton itself. I believe python's [dict implementation](https://github.com/PiJoules/cpython-modified/blob/master/Objects/dictobject.c) uses a combination of open addressing and resizing the array if 2/3 of the array is occupied.

### Operations

#### Lookup
This involves checking if an element for a given key exists in the hash table, which is essentially just running the key through the hash function. If chaining or open addressing is implemented, in order to retrive the proper element for a given key, the value of the key is also compared against against any subsequent value in the list or probe sequence, making the time complexity for lookup linear in worst case. This can be avaided though by resizing the array if a certain capacity threshold is reached to reduce the number of collisions.

#### Insertion/Updating
This involves inserting a value for a given key at an index in the array. If open addressing or chaining is implemented, and a collision occurs, the value is instead placed at the end of the list or the next avaialble spot found through probing.

#### Deletion
This varies depending on implementation. From a high level perspective, deleting the element could just mean setting the value at the hash to be NULL and decreasing a counter for the length of the array by 1. If separate chaining is implemented, deletion on the list implementation will take place for the given key and may involve iterating over the whole list. If open addressing is implemented, you will need to replace the deleted with a marker indicating the offset of the next element that should be checked as a result of probing.

### Complexity
The main benefits behind hash tables are constant lookup, insertion, and deletion time. In the worst case scenario, when a bad hash funciton is used, the number of values for a given key can increase linearly, effectively making lookup time complexity that of whatever you implemented to ammend collision, but this can be countered by resizing the hash table. For average and best case scenarios, these operations are effectively done in constant time.

The cost of the hash table though is the amount of space needed. In order to support a large number of hashes, a large array will be needed to store all the elements. Objects in python are actually implemented as dictionaries in the underlying C code, and since everything in python is an object, this is one of the reasons for why python programs typically use much more memory than other languages.
