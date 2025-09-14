const { PrismaClient } = require('@prisma/client')
const bcrypt = require('bcryptjs')
const prisma = new PrismaClient()

async function main() {
  const email = 'admin@ferapp.local'
  const name = 'Admin'
  const password = 'admin123' // dev only
  const passwordHash = await bcrypt.hash(password, 10)
  await prisma.user.upsert({
    where: { email },
    create: { email, name, passwordHash, role: 'ADMIN' },
    update: {}
  })
  console.log(`Seeded admin: ${email} / ${password}`)
}

main().finally(() => prisma.$disconnect())
