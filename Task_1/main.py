class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def print_list(self):
        current = self.head
        values = []
        while current:
            values.append(str(current.data))
            current = current.next
        print(" -> ".join(values) if values else "(порожній список)")

    def reverse(self):
        """Реверсує список, змінюючи посилання між вузлами."""
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def insertion_sort(self):
        """Сортує список вставками через перепідключення вузлів."""
        dummy = Node()
        current = self.head

        while current:
            next_node = current.next
            current.next = None

            prev = dummy
            while prev.next and prev.next.data < current.data:
                prev = prev.next

            current.next = prev.next
            prev.next = current
            current = next_node

        self.head = dummy.next

    @staticmethod
    def merge_sorted(list1: "LinkedList", list2: "LinkedList") -> "LinkedList":
        """Об'єднує два відсортовані списки в один відсортований."""
        dummy = Node()
        tail = dummy

        l1 = list1.head
        l2 = list2.head

        while l1 and l2:
            if l1.data <= l2.data:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next

        tail.next = l1 if l1 else l2

        merged = LinkedList()
        merged.head = dummy.next
        return merged


if __name__ == "__main__":
    print("=== Реверсування ===")
    reverse_list = LinkedList()
    for value in (15, 10, 5, 20, 25):
        reverse_list.insert_at_beginning(value)
    print("До реверсу:")
    reverse_list.print_list()
    reverse_list.reverse()
    print("Після реверсу:")
    reverse_list.print_list()

    print("\n=== Сортування вставками ===")
    sort_list = LinkedList()
    for value in (15, 10, 5, 20, 25):
        sort_list.insert_at_beginning(value)
    print("До сортування:")
    sort_list.print_list()
    sort_list.insertion_sort()
    print("Після сортування:")
    sort_list.print_list()

    print("\n=== Об'єднання двох відсортованих списків ===")
    list_a = LinkedList()
    for value in (1, 3, 5):
        list_a.insert_at_end(value)

    list_b = LinkedList()
    for value in (2, 4, 6):
        list_b.insert_at_end(value)

    print("Список A:")
    list_a.print_list()
    print("Список B:")
    list_b.print_list()

    merged = LinkedList.merge_sorted(list_a, list_b)
    print("Об'єднаний список:")
    merged.print_list()
