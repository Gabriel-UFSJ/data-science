class Project:
    def __init__(self, complexity, time_frame, members):
        self.complexity = complexity
        self.time_frame = time_frame
        self.members = members
        self.hourly_rate = 18.75

    def calculate_price(self):
        if self.complexity == "low":
            complexity_multiplier = 1
        elif self.complexity == "mid":
            complexity_multiplier = 1.5
        elif self.complexity == "high":
            complexity_multiplier = 2

        time_frame_multiplier = self.time_frame / 3

        members_multiplier = self.members / 3

        price = self.hourly_rate * 160 * complexity_multiplier * time_frame_multiplier * members_multiplier

        return price
