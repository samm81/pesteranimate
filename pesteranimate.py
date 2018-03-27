import click
import requests
import sys
from datetime import datetime
from time import sleep
from concurrent.futures import ThreadPoolExecutor

lines = []
done = False

def animate_lines(speed):
    def getdt(dtstr):
        return datetime.strptime(dtstr.replace('  ', ' '), '%a %b %d %X %Z %Y')
    prevdt = None
    while not done or len(lines) > 1:
        while len(lines) < 1:
            pass
        line = lines.pop(0)
        dtstr, message = line.split('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        dt = getdt(dtstr)
        if not prevdt:
            prevdt = dt
        timegap = prevdt - dt
        wait = timegap.total_seconds() / (300 * speed)
        sleep(wait)
        click.secho(message, fg='yellow')
        prevdt = dt

def get_lines(userid):
    url = 'https://acb15c35.ngrok.io/users/{}'.format(userid)
    click.secho('connecting to pesterbot servers...', fg='blue')
    sleep(.6)
    r = requests.get(url, stream=True)
    total_length = r.headers.get('content-length')
    if r.status_code != 200 or total_length is None:
        click.secho('error connecting to pesterbot servers', fg='red')
        sys.exit(1)
    click.secho('retrieving information for user {}...'.format(userid), fg='blue')
    if r.encoding is None:
        r.encoding = 'utf-8'
    chunk_size = 1024
    total_length = int(total_length)
    overflow = ''
    for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size, decode_unicode=True)):
        if i is 0:
            chunk = chunk[86:]
        if i is total_length // chunk_size:
            chunk = chunk[:-17] # TODO
        chunk = overflow + chunk
        lines_ = chunk.split('<br/>')
        overflow = lines_[-1]
        lines_ = lines_[:-1]
        lines.extend(lines_)

@click.command()
@click.option('--userid', type=int, default=975815712488213, help='User ID of pesterbot user (can be found in the URL of response page)')
@click.option('--speed', type=int, default=1, help='Speed mutltiplier of how fast to display the statuses')
def animate(userid, speed):
    with ThreadPoolExecutor(max_workers=2) as pool:
        get_lines_future = pool.submit(get_lines, userid)
        animate_lines_future = pool.submit(animate_lines, speed)
        def done_(future):
            done = True
        get_lines_future.add_done_callback(done_)
        return animate_lines_future.result()

if __name__ == '__main__':
    animate()
