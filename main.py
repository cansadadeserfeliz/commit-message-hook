#!/usr/bin/python3
import sys
import re
from subprocess import check_output

TICKET_NUMMER_RE = re.compile(r'\d{9,11}')
BRANCH_TYPE_RE = re.compile(r'(feature)|(fix)|(hotfix)|(refactor)', re.I)


def format_commit_message(commit_msg_lines, branch_name):
    first_commit_msg_line = commit_msg_lines[0]

    ticket_number_match = TICKET_NUMMER_RE.search(branch_name)
    if ticket_number_match:
        ticket_number = ticket_number_match.string[
            ticket_number_match.start():ticket_number_match.end()
        ]
    else:
        ticket_number = 'NA'

    ticket_type_match = BRANCH_TYPE_RE.search(branch_name)
    if ticket_number_match:
        ticket_type = ticket_type_match.string[
            ticket_type_match.start():ticket_type_match.end()
        ].upper()
    else:
        ticket_type = 'NA'

    # Override the first line
    commit_msg_lines[0] = f'[{ticket_type}][{ticket_number}] {first_commit_msg_line}'
    return commit_msg_lines


def main():
    commit_msg_fn = sys.argv[1]
    commit_msg_lines = [
        line
        for line in open(commit_msg_fn, encoding='utf-8').readlines()
    ]

    current_branch_name = check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    ).decode('utf-8')

    commit_msg_lines = format_commit_message(
        commit_msg_lines=commit_msg_lines,
        branch_name=current_branch_name,
    )

    with open(commit_msg_fn, 'w', encoding='utf-8') as commit_file:
        for line in commit_msg_lines:
            commit_file.write(line)


if __name__ == '__main__':
    main()
