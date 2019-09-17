class Sorting:

    # dataList: 입력 data set, orderBase: 정렬 기준 되는 인자, reverseYn: 내림차순 정렬 여부
    def sortingListSimpleValue(self, dataGroupList, orderBase, reverseYn):

        # 전체 파일 리스트를 base 기준 sort
        sortedGrooupLists = sorted(dataGroupList, key=lambda k: k[orderBase], reverse=reverseYn)

        # sort 결과에 따라 순위 부여
        order = 0
        for sortedGrooup in sortedGrooupLists:

            order = order + 1
            sortedGrooup[orderBase+'_order'] = order

        return sortedGrooupLists


    # dataList: 입력 data set, orderBase: 정렬 기준 되는 인자, reverseYn: 내림차순 정렬 여부
    def sortingListComplexValue(self, dataGroupList):
        sorting = Sorting()

        # 전체파일 리스트에서 per과 roa순위를 단순 합산
        for dataGroup in dataGroupList:
            dataGroup['final'] = dataGroup['per_order']+dataGroup['roa_order']

        resultList = sorting.sortingListSimpleValue(dataGroupList, 'final', False)

        return resultList