import os
import re

#
# EVIL PYTHON
#

problem_links = dict()
solutions = dict()
decision_driver_links = dict()
num_refs = 0
participating_members = dict()
for root, dirs, files in os.walk("./memo", topdown=False):
    for file in files:
        if file.endswith(".md"):
            num_refs += 1
            participating_members.setdefault(file[4:-3], 0)
            participating_members[file[4:-3]] += 1
            md_file = os.path.join(root, file).replace("\\", "/")
            with open(md_file, "r") as f:
                content = f.read()
                start = content.lower().find("## problem") + 10
                end = content.find("##", start)
                start_with_dash = None
                lines = [x for x in content[start:end].strip().splitlines() if x]
                problem_num = 1
                for line in lines:
                    line = line.replace("*", "").strip()
                    problem = (
                        line[line.find(next(filter(str.isalpha, line))) :]
                        .capitalize()
                        .split(":")[0]
                        .strip()
                    )
                    if problem.endswith("."):
                        problem = problem[:-1]
                    if problem.lower().endswith("problem"):
                        problem = problem[:-7].strip()
                    if not problem.lower().endswith("ss") and problem.lower().endswith(
                        "s"
                    ):
                        problem = problem[:-1]
                    if start_with_dash is None:
                        start_with_dash = line.startswith("-")
                    if (
                        (start_with_dash and line.startswith("-"))
                        or (not start_with_dash and line[0].isdigit())
                        or len(lines) == 1
                    ):
                        if line[0].isdigit():
                            problem_num = int(line[0])
                        problem_links.setdefault(problem, []).append((file, md_file))
                        sol_start = (
                            content.lower().find(f"problem {problem_num}")
                            + 8
                            + len(str(problem_num))
                        )
                        if (
                            sol_start < 10 - len(str(problem_num))
                            and content[end:].find("problem") == -1
                        ):
                            sol_start = content.lower().find(f"solution") + 8
                        elif sol_start < 10 - len(str(problem_num)):
                            sol_start = (
                                content.lower().find(f"solution {problem_num}")
                                + 9
                                + len(str(problem_num))
                            )
                        if sol_start < 10 + len(str(problem_num)):
                            continue
                        sol_end = content.find("##", sol_start)
                        sol_lines = [
                            x.strip()
                            for x in content[sol_start:sol_end].splitlines()
                            if x.strip()
                        ]
                        for sol in sol_lines:
                            sol = sol.replace("*", "")
                            sol_text = (
                                sol[sol.find(next(filter(str.isalpha, sol))) :]
                                .capitalize()
                                .strip()
                            )
                            sol_text = re.sub(r"\[\^\d.?\]", "", sol_text)
                            if sol_text.endswith("."):
                                sol_text = sol_text[:-1]
                            if sol_text.lower() != "n/a":
                                solutions.setdefault(problem, []).append(
                                    f"{sol_text}. ([{file[:-3]}]({md_file}))"
                                )
                        problem_num += 1
                    else:
                        continue
                start = content.lower().find("## decision driver") + 18
                end = content.find("##", start)
                lines = [
                    x.strip()
                    for x in content[start:end].strip().splitlines()
                    if x.strip()
                ]
                for line in lines:
                    line = line.replace("*", "")
                    decision_driver = (
                        line[line.find(next(filter(str.isalpha, line))) :]
                        .capitalize()
                        .strip()
                    )
                    decision_driver = re.sub(r"\(.*?\)", "", decision_driver).strip()
                    if decision_driver.endswith("."):
                        decision_driver = decision_driver[:-1]
                    if decision_driver.lower() != "n/a":
                        decision_driver_links.setdefault(decision_driver, []).append(
                            (file, md_file)
                        )


with open("conclusion.md", "w") as out_file:
    out_file.write(f"# Conclusion\n")
    out_file.write("| Student No. | References |\n|---|---|\n")
    for k, v in participating_members.items():
        out_file.write(f"|{k}|{v}|\n")
    out_file.write(f"#### Total references: {num_refs}\n## Problems\n")
    for i, k in enumerate(sorted(problem_links.keys())):
        links = problem_links.get(k)
        out_file.write(
            f"- **Problem {i + 1}**: {k} ({', '.join([f'[{link[0][:-3]}]({link[1]})' for link in links])})\n"
        )
        problem_sols = solutions.get(k, None)
        if problem_sols:
            for solution in problem_sols:
                out_file.write(f"\t- {solution}\n")
    out_file.write("## Decision Drivers\n")
    for k in sorted(decision_driver_links.keys()):
        links = decision_driver_links.get(k)
        out_file.write(
            f"- {k} ({', '.join([f'[{link[0][:-3]}]({link[1]})' for link in links])})\n"
        )
