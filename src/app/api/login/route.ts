import { NextResponse } from 'next/server';
import dbConnect from '../../../lib/mongodb';
import User from '../../../models/User';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

export async function POST(req: Request) {
  const { email, password } = await req.json();

  if (!process.env.JWT_SECRET) {
    return NextResponse.json({ error: 'JWT_SECRET is not defined' }, { status: 500 });
  }

  await dbConnect();

  const user = await User.findOne({ email });

  if (!user) {
    return NextResponse.json({ error: 'No user found' }, { status: 400 });
  }

  const isValid = await bcrypt.compare(password, user.password);

  if (!isValid) {
    return NextResponse.json({ error: 'Invalid password' }, { status: 400 });
  }

  const token = jwt.sign({ email: user.email }, process.env.JWT_SECRET, { expiresIn: '1h' });

  return NextResponse.json({ token });
}
