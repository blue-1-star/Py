nums=[5,10,1,60,25,3]
print("Список из чисел:", nums)
print("Длина списка:", len(nums))
print("Max=", max(nums)," sum=",sum(nums))
print("Обратный порядок:", list(reversed(nums)))
print("Sorted increasing:", sorted(nums))
print("Сортировка по убыванию:", sorted(nums, reverse=True))
nums[1] = "Текст"
print(nums)
print("Get slice:", nums[1:len(nums)-1])
nums[1:-1]=["A","B"]
print("After change:",nums)
nums= list(range(5,11))
print("list of digits from 5 to 10:\n",nums)
nums =[2*k+1 for k in range(5)]
print("odd numbers:", nums)
