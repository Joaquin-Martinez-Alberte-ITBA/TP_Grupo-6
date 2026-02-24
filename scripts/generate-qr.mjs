import QRCode from 'qrcode';

const url = process.argv[2] ?? 'http://localhost:3000/checkin?site=site-central';
const out = process.argv[3] ?? 'public/checkin-qr.png';

await QRCode.toFile(out, url, { margin: 1, width: 400 });
console.log(`QR generado en ${out} para ${url}`);
