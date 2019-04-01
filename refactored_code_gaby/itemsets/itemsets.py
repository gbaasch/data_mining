class Itemsets:
    def __init__(self, df):
        """ Create a dict of itemsets out of a pandas dataframe that includes
        a objects and associated items. Makes dict like
        {
            object_1: {item_1, item_2},
            object_2: {item_1},
            ....
        }
        """
        self.itemsets = {}
        self.create_itemsets(df)

    def create_itemsets(self, df):
        for _, row in df.iterrows():
            object = row[0]
            item = row[1]
            items = self.itemsets.get(object)
            if items is None:
                self.itemsets[object] = {item}
            else:
                items.add(item)
                self.itemsets[object] = items
