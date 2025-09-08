from django.test import TestCase
from .models import Run, RunInputFile, RunOutputArtifact
from django.core.files.uploadedfile import SimpleUploadedFile

class RunModelTest(TestCase):
    def test_run_creation(self):
        run = Run.objects.create(user_input='Test input', status='pending')
        self.assertEqual(run.user_input, 'Test input')
        self.assertEqual(run.status, 'pending')
        self.assertIsNone(run.final_output)
        self.assertIsNone(run.completed_at)
        self.assertTrue(str(run).startswith('Run'))

class RunInputFileModelTest(TestCase):
    def test_input_file_creation(self):
        run = Run.objects.create(user_input='Test input')
        uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        run_input_file = RunInputFile.objects.create(
            run=run,
            file=uploaded_file,
            file_type='pdf',
            description='Test PDF file'
        )
        self.assertEqual(run_input_file.file_type, 'pdf')
        self.assertTrue(str(run_input_file).startswith('PDF'))

class RunOutputArtifactModelTest(TestCase):
    def test_output_artifact_creation(self):
        run = Run.objects.create(user_input='Test input')
        artifact_data = {"foo": "bar"}
        artifact = RunOutputArtifact.objects.create(
            run=run,
            artifact_type='chart',
            data=artifact_data,
            title='Test Chart'
        )
        self.assertEqual(artifact.artifact_type, 'chart')
        self.assertEqual(artifact.data, artifact_data)
        self.assertEqual(artifact.title, 'Test Chart')
        self.assertTrue(str(artifact).startswith('chart'))
