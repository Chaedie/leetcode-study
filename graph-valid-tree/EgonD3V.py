from typing import List
from unittest import TestCase, main


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def valid_tree(self, n: int, edges: List[List[int]]) -> bool:
        return self.solve_union_find(n, edges)

    """
    LintCode 로그인이 안되어서 https://neetcode.io/problems/valid-tree에서 실행시키고 통과만 확인했습니다.
    
    Runtime: ? ms (Beats ?%)
    Time Complexity: O(max(m, n))
        - UnionFind의 parent 생성에 O(n)
        - edges 조회에 O(m)
            - Union-find 알고리즘의 union을 매 조회마다 사용하므로, * O(α(n)) (α는 아커만 함수의 역함수)
        - UnionFind의 모든 노드가 같은 부모, 즉 모두 연결되어 있는지 확인하기 위해, n번 find에 O(n * α(n))
        > O(n) + O(m * α(n)) + O(n * α(n)) ~= O(max(m, n) *  α(n)) ~= O(max(m, n)) (∵ α(n) ~= C)

    Memory: ? MB (Beats ?%)
    Space Complexity: O(n)
        - UnionFind의 parent와 rank가 크기가 n인 리스트이므로, O(n) + O(n)
        > O(n) + O(n) ~= O(n)
    """
    def solve_union_find(self, n: int, edges: List[List[int]]) -> bool:

        class UnionFind:
            def __init__(self, size: int):
                self.parent = [i for i in range(size)]
                self.rank = [1] * size

            def union(self, first: int, second: int) -> bool:
                first_parent, second_parent = self.find(first), self.find(second)
                if first_parent == second_parent:
                    return False

                if self.rank[first_parent] > self.rank[second_parent]:
                    self.parent[second_parent] = first_parent
                elif self.rank[first_parent] < self.rank[second_parent]:
                    self.parent[first_parent] = second_parent
                else:
                    self.parent[second_parent] = first_parent
                    self.rank[first_parent] += 1

                return True

            def find(self, node: int):
                if self.parent[node] != node:
                    self.parent[node] = self.find(self.parent[node])

                return self.parent[node]

        unionFind = UnionFind(size=n)
        for first, second in edges:
            is_cycle = unionFind.union(first, second) is False
            if is_cycle:
                return False

        root = unionFind.find(0)
        for i in range(1, n):
            if unionFind.find(i) != root:
                return False

        return True


class _LeetCodeTestCases(TestCase):
    def test_1(self):
        n = 5
        edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
        output = False

        self.assertEqual(Solution().valid_tree(n, edges), output)


if __name__ == '__main__':
    main()
