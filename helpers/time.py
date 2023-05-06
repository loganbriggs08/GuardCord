import pendulum

class Time:
    def to_human_time(time: str) -> str:
        datetime = pendulum.parse(time)
        
        return datetime.diff_for_humans()