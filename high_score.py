

class HighScore:

    @staticmethod
    def get_max():
        with open("high_scores.txt", 'r') as f:
            lines = f.readlines()
            int_list = []
            for line in lines:
                int_list.append(int(line.strip()))
        return max(int_list)
    
    @staticmethod
    def write(text):
        with open("high_scores.txt", 'a') as f:
            f.write(str(text) + "\n")
