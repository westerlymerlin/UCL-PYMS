"""Test generator for new batches"""
from batchclass import batch


def commit_planchet(description):
    """

    :param description: The description of the planchet
    :return: None

    This method commits a planchet in the system. It takes a description as input and uses it to create a new planchet
     batch with the given description. It then adds steps for different locations and sample identifiers.
     Finally, it saves the batch.

    Example Usage:
        >>> commit_planchet("Planchet for testing")

    """
    batch.cancel()
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



def commit_q(description):
    """
    Commits a new batch with a description and a series of 10 Q shots.
    """
    batch.cancel()
    batch.new('simple', description)
    batch.addstep('Line Clean','','')
    batch.addstep('Line Blank', '', '')
    for _ in range (10):
        batch.addstep('Q-Standard', '', '')
    batch.addstep('Line Blank', '', '')
    batch.save()


if __name__ == '__main__':
    descriptiontext = input('Enter the test description: ')
    batch_type = input('Planchet (p) or Qshots (q)? ')
    if len(descriptiontext) > 0 and batch_type.lower() == 'p':
        commit_planchet(descriptiontext)
        print('New test planchet created')
    elif len(descriptiontext) > 0 and batch_type.lower() == 'q':
        commit_q(descriptiontext)
        print('New test Qlist created')
