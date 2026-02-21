"""
Test batch generator for analytical system automation.

This module provides utilities to programmatically create standardized test batches
for an analytical system. It supports two types of test configurations:

1. Planchet batches - Creates a comprehensive test sequence with 56 steps covering
   special locations (S1-S6) and a full 7x7 grid (A1-G7) for systematic sample analysis
2. Q-standard batches - Creates simple calibration sequences with line cleaning,
   blanks, and number of Q-standard measurements

Both batch types follow predefined analytical protocols and automatically generate
sequential sample identifiers. The module can be run interactively via command line
or imported for programmatic batch creation.

Functions:
    commit_planchet(description): Creates a 56-step planchet test batch
    commit_q(description): Creates a Q-standard calibration batch
"""
from batchclass import batch


def commit_planchet(description):
    """
   This method commits a planchet in the system. It takes a description as input and uses it to create a new planchet
     batch with the given description. It then adds steps for different locations and sample identifiers.
     Finally, it saves the batch.

    Example Usage:
        >>> commit_planchet("Planchet for testing")

    """
    batch.cancel_batch()
    batch.new('planchet', description)
    counter = 1
    for i in range(1, 4):
        location = 'S' + str(i)
        sampleid = 'DUR%02i' % counter
        counter += 1
        print(location, sampleid)
        batch.addstep('Apatite + Reheat', location, sampleid)
    for row in 'ABCDEFG':
        for i in range(1, 8):
            location = row + str(i)
            sampleid = 'Sample%02i' % counter
            counter += 1
            print(location, sampleid)
            batch.addstep('Apatite + Reheat', location, sampleid)
    for i in range(4, 7):
        location = 'S' + str(i)
        sampleid = 'DUR%02i' % counter
        counter += 1
        print(location, sampleid)
        batch.addstep('Apatite + Reheat', location, sampleid)
    batch.save()


def commit_q(description, qshot_qty=10):
    """
    Commits a new batch with a description and a series of Q shots.
    """
    batch.cancel_batch()
    batch.new('simple', description)
    batch.addstep('Line Blank', '', '')
    counter =0
    for _ in range (qshot_qty):
        batch.addstep('Q-Standard', '', '')
        counter += 1
        if counter == 25:
            batch.addstep('Pump', '', '')
            batch.addstep('Line Blank', '', '')
            counter = 0
    batch.addstep('Line Blank', '', '')
    batch.save()

def commit_des_pair(description, des_pair_qty=3):
    """
    Commits a new batch with a description and a series of Des Q and D shots.
    """
    batch.cancel_batch()
    batch.new('simple', description)
    batch.addstep('Line Blank', '', '')
    counter =0
    for _ in range (des_pair_qty):
        batch.addstep('Q-Des', '', '')
        batch.addstep('D-Des-2', '', '')
        counter += 1
        if counter == 20:
            batch.addstep('Pump', '', '')
            batch.addstep('Line Blank', '', '')
            counter = 0
    batch.addstep('Line Blank', '', '')
    batch.save()

if __name__ == '__main__':
    descriptiontext = input('Enter the test description: ')
    batch_type = input('Planchet (p), Qshots (q) or Des pairs (Q-Des followed by D-Des-2) (d)? ')
    if batch_type.lower() == 'q':
        number_of_qshots = int(input('Enter the number of Qshots to run: '))
        print('New test Qlist created')
        commit_q(descriptiontext, number_of_qshots)
    if batch_type.lower() == 'd':
        number_of_des_pairs = int(input('Enter the number of Des pairs to run: '))
        print('New test Des pair list created')
        commit_des_pair(descriptiontext, number_of_des_pairs)
    if len(descriptiontext) > 0 and batch_type.lower() == 'p':
        commit_planchet(descriptiontext)
        print('New test planchet created')
