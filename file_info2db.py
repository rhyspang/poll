#   annotator_audio
#   --------------------------------------
#
#   Written and maintained by Rhys Pang <rhyspang@qq.com>
#
#   Copyright 2018 rhys. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import os

import pymysql

args = argparse.ArgumentParser()
args.add_argument('-d', '--directory', default="poll/static/low_score",
                  help="file directory")
args.add_argument('-b', '--batch', type=int, default=1000,
                  help="save batch size")
args.add_argument('-m', '--max_file', type=int, default=1000,
                  help="max file number per word")
FLAGS = args.parse_args()

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='password',
    db='poll'
)


def insert(file_path, prediction):

    SQL = "INSERT INTO labelling_files(prediction, file_uri) " \
          "SELECT * FROM (SELECT '%s', '%s') AS tmp " \
          "WHERE NOT EXISTS " \
          "(SELECT id FROM labelling_files WHERE file_uri = '%s')"
    with conn.cursor() as cursor:
        cursor.execute(SQL, (prediction, file_path, file_path))


def main():

    cnt = 0
    for root, dirs, files in os.walk(FLAGS.directory):
        word_cnt = 0
        for filename in files:
            cnt += 1
            word_cnt += 1

            file_path = os.path.join(root, filename).split(os.sep)[-3:]
            prediction = file_path[-2]
            file_path = os.sep.join(file_path)
            # print(file_path, prediction)
            insert(file_path, prediction)
            if cnt % FLAGS.batch == 0:
                print('%s files to db' % cnt)
                conn.commit()
            if word_cnt >= FLAGS.max_file:
                break
    conn.commit()
    print('%s files to db' % cnt)


if __name__ == '__main__':
    main()
