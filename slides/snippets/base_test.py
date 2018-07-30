# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import sys
import unittest
import httplib2
from apiclient import discovery
from oauth2client.client import GoogleCredentials
from googleapiclient import errors

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = cls.create_credentials()
        http = cls.credentials.authorize(httplib2.Http())
        cls.credentials.refresh(http)
        cls.service = discovery.build('slides', 'v1', http=http)
        cls.drive_service = discovery.build('drive', 'v3', http=http)
        cls.sheets_service = discovery.build('sheets', 'v4', http=http)
        # Hide STDOUT output generated by snippets.
        cls.stdout = sys.stdout
        sys.stdout = None

    @classmethod
    def tearDownClass(cls):
        # Restore STDOUT.
        sys.stdout = cls.stdout

    @classmethod
    def create_credentials(cls):
        credentials = GoogleCredentials.get_application_default()
        scope = [
            'https://www.googleapis.com/auth/drive',
        ]
        return credentials.create_scoped(scope)

    def setUp(self):
        self.files_to_delete = []

    def tearDown(self):
        for file_id in self.files_to_delete:
            try:
                self.drive_service.files().delete(fileId=file_id).execute()
            except errors.HttpError:
                print('Unable to delete file %s' % file_id, file=sys.stderr)

    def delete_file_on_cleanup(self, file_id):
        self.files_to_delete.append(file_id)

    def create_test_presentation(self):
        presentation = {
            'title': 'Test Preso'
        }
        presentation = self.service.presentations().create(
            body=presentation).execute()
        self.delete_file_on_cleanup(presentation.get('presentationId'))
        return presentation.get('presentationId')

    def add_slides(self, presentation_id, num, layout='TITLE_AND_TWO_COLUMNS'):
        requests = []
        slide_ids = []
        for i in range(num):
            slide_id = 'slide_{0}'.format(i)
            slide_ids.append(slide_id)
            requests.append({
                'createSlide': {
                    'objectId': slide_ids[i],
                    'slideLayoutReference': {
                        'predefinedLayout': layout
                    }
                }
            })
        body = {
            'requests': requests
        }
        response = self.service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        return slide_ids

    def create_test_textbox(self, presentation_id, page_id):
        box_id = 'MyTextBox_01'
        pt350 = {
            'magnitude': 350,
            'unit': 'PT'
        }
        requests = []
        requests.append({
            'createShape': {
                'objectId': box_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': pt350,
                        'width': pt350
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 350,
                        'translateY': 100,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': box_id,
                'insertionIndex': 0,
                'text': 'New Box Text Inserted'
            }
        })

        body = {
            'requests': requests
        }
        response = self.service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        return response.get('replies')[0].get('createShape').get('objectId')

    def create_test_sheets_chart(
        self, presentation_id, page_id, spreadsheet_id, sheet_chart_id):
        chart_id = 'MyChart_01'
        emu4M = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }
        requests = []
        requests.append({
            'createSheetsChart': {
                'objectId': chart_id,
                'spreadsheetId': spreadsheet_id,
                'chartId': sheet_chart_id,
                'linkingMode': 'LINKED',
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': emu4M,
                        'width': emu4M
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 100000,
                        'translateY': 100000,
                        'unit': 'EMU'
                    }
                }
            }
        })

        body = {
            'requests': requests
        }
        response = self.service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        return response.get('replies')[0] \
            .get('createSheetsChart').get('objectId')

if __name__ == '__main__':
    unittest.main()
