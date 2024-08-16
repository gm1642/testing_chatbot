import { NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';

export async function GET(req: Request) {
  const authHeader = req.headers.get('authorization');

  if (!authHeader) {
    return NextResponse.json({ error: 'No token provided' }, { status: 401 });
  }

  const token = authHeader.split(' ')[1];

  if (!process.env.JWT_SECRET) {
    console.error('JWT_SECRET is not defined');
    return NextResponse.json({ error: 'JWT_SECRET is not defined' }, { status: 500 });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return NextResponse.json({ email: (decoded as any).email });
  } catch (error) {
    console.error('Invalid token', error);
    return NextResponse.json({ error: 'Invalid token' }, { status: 401 });
  }
}
