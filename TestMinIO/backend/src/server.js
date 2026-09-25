import express from 'express';
import cors from 'cors';
import multer from 'multer';
import * as Minio from 'minio';
import fs from 'fs';
import path from 'path';

const app = express();
const PORT = 5000;
const BUCKET_NAME = 'test-bucket';

app.use(cors());
app.use(express.json());

// 1. Cấu hình MinIO Client
const minioClient = new Minio.Client({
  endPoint: 'localhost',
  port: 9000,
  useSSL: false,
  accessKey: 'admin',
  secretKey: 'password123',
});

// Tự động khởi tạo bucket và public read policy
const initBucket = async () => {
  try {
    const exists = await minioClient.bucketExists(BUCKET_NAME);
    if (!exists) {
      await minioClient.makeBucket(BUCKET_NAME, 'us-east-1');
      // Set policy để file có thể truy cập public trực tiếp qua link
      const policy = {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: { AWS: ['*'] },
            Action: ['s3:GetObject'],
            Resource: [`arn:aws:s3:::${BUCKET_NAME}/*`],
          },
        ],
      };
      await minioClient.setBucketPolicy(BUCKET_NAME, JSON.stringify(policy));
      console.log(`Bucket '${BUCKET_NAME}' created with public read policy.`);
    }
  } catch (err) {
    console.error('Error initializing MinIO bucket:', err);
  }
};
initBucket();

// Cấu hình Multer lưu file tạm vào RAM
const upload = multer({ storage: multer.memoryStorage() });

// Thư mục chứa data txt
const DATA_DIR = './data';
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 2. API Upload File
app.post('/api/upload', upload.single('file'), async (req, res) => {
  try {
    const { username } = req.body;
    const file = req.file;

    if (!username || !file) {
      return res.status(400).json({ error: 'Username and file are required.' });
    }

    const objectName = `${Date.now()}-${file.originalname}`;

    // Upload lên MinIO
    await minioClient.putObject(
      BUCKET_NAME,
      objectName,
      file.buffer,
      file.size,
      { 'Content-Type': file.mimetype }
    );

    const fileUrl = `http://localhost:9000/${BUCKET_NAME}/${objectName}`;

    // Ghi link vào file {username}.txt
    const filePath = path.join(DATA_DIR, `${username}.txt`);
    fs.appendFileSync(filePath, `${fileUrl}\n`);

    res.json({ message: 'Upload success', url: fileUrl });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to upload file' });
  }
});

// 3. API Lấy danh sách link file của user
app.get('/api/files/:username', (req, res) => {
  try {
    const { username } = req.params;
    const filePath = path.join(DATA_DIR, `${username}.txt`);

    if (!fs.existsSync(filePath)) {
      return res.json({ files: [] });
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const files = content
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean);

    res.json({ files });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to fetch files' });
  }
});

app.listen(PORT, () => {
  console.log(`Backend is running on http://localhost:${PORT}`);
});