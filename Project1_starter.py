from datetime import datetime
import ast

# Helper functions for reading and formatting data
def get_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return [line for line in lines if line]

def reformatted_string(data):
    data = data.replace("':'", "','")
    return ast.literal_eval(data)

# Functions for combining, sorting, and merging schedules
def combine_schedules(*schedules):
    output = []
    for schedule in schedules:
        if isinstance(schedule[0], list):
            output.extend(schedule)
        else:
            output.append(schedule)
    return output

def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    merged = []
    while left and right:
        if left[0][0] <= right[0][0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
    merged.extend(left)
    merged.extend(right)
    return merged

# Functions for handling busy and work schedules, identifying free slots, and checking duration
def merge_schedules(schedule, schedule_type):
    updated_schedule = [schedule[0]]
    index = 0
    for entry in schedule[1:]:
        start_time = datetime.strptime(entry[0], "%H:%M").time()
        end_time = datetime.strptime(entry[1], "%H:%M").time()
        max_time = datetime.strptime(updated_schedule[index][1], "%H:%M").time()

        if schedule_type == "busy":
            if start_time <= max_time and end_time > max_time:
                updated_schedule[index][1] = entry[1]
            elif start_time > max_time:
                index += 1
                updated_schedule.append(entry)
        elif schedule_type == "work":
            if start_time <= max_time and end_time < max_time:
                updated_schedule[index][1] = entry[1]
            elif start_time > max_time:
                index += 1
                updated_schedule.append(entry)

    return updated_schedule

def getFreeSchedules(free, busy):
    output = free
    index = 0
    for free_slot in range(len(free)):
        for busy_slot in range(len(busy)):
            min_time = datetime.strptime(output[index][0], '%H:%M')
            max_time = datetime.strptime(output[index][1], '%H:%M')
            start_block = datetime.strptime(busy[busy_slot][0], '%H:%M')
            if (start_block == min_time):
                output[index] = [busy[busy_slot][1], free[free_slot][1]]

            elif (start_block <= max_time):
                output.append([busy[busy_slot][1], output[index][1]])
                output[index][1] = busy[busy_slot][0]
                index += 1
    return(output)

def verify_duration(schedules, duration):
    valid_schedules = []
    for schedule in schedules:
        time_a = datetime.strptime(schedule[0], "%H:%M")
        time_b = datetime.strptime(schedule[1], "%H:%M")
        if int((time_b - time_a).total_seconds() // 60) >= duration:
            valid_schedules.append(schedule)
    return valid_schedules

# Main function that reads, processes, and outputs results
def main(inp):

    f = open("output.txt", "w")
    f.write("")
    f.close()

    repeat = len(inp)/5
    for i in range(int(repeat)):
        person1_busy_schedule = reformatted_string(inp[i*5 + 0])
        person2_busy_schedule = reformatted_string(inp[i*5 + 2])
        person1_work_hours = reformatted_string(inp[i*5 + 1])
        person2_work_hours = reformatted_string(inp[i*5 + 3])
        meeting_duration = reformatted_string(inp[i*5 + 4])

        busy = combine_schedules(person1_busy_schedule, person2_busy_schedule)
        busy = merge_sort(busy)
        busy = merge_schedules(busy, "busy")
       
        work = combine_schedules(person1_work_hours, person2_work_hours)
        work = merge_sort(work)
        work = merge_schedules(work, "work")
        work = getFreeSchedules(work, busy)
        work = verify_duration(work, meeting_duration)

        f = open("output.txt", "a")
        if (str(work) == "[]"):
            work = ["Sorry - no times are available for the provided duration"]
        f.write("Case: " + str(i + 1) + "\n" + str(work) + "\n\n")
        f.close()

    f = open("output.txt", "r")
    print(f.read())

main(get_input("input.txt"))

