#!/bin/bash

# Migration Script: SQLite to PostgreSQL
# This script helps migrate your data from SQLite to PostgreSQL

echo "🔄 Starting migration from SQLite to PostgreSQL..."
echo ""

# Step 1: Backup SQLite data
echo "📦 Step 1: Exporting data from SQLite..."
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude contenttypes \
    --exclude auth.Permission \
    --indent 4 \
    > data_backup.json

if [ $? -eq 0 ]; then
    echo "✅ Data exported successfully to data_backup.json"
else
    echo "❌ Failed to export data"
    exit 1
fi

echo ""

# Step 2: Set up PostgreSQL
echo "🗄️  Step 2: Setting up PostgreSQL database..."
echo "⚠️  Make sure you have set DATABASE_URL in your .env file"
echo "   Example: DATABASE_URL=postgresql://user:password@host/database"
echo ""
read -p "Press Enter when DATABASE_URL is configured in .env..."

# Step 3: Run migrations on PostgreSQL
echo ""
echo "🔨 Step 3: Running migrations on PostgreSQL..."
python manage.py migrate

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi

# Step 4: Import data
echo ""
echo "📥 Step 4: Importing data into PostgreSQL..."
python manage.py loaddata data_backup.json

if [ $? -eq 0 ]; then
    echo "✅ Data imported successfully"
else
    echo "❌ Data import failed"
    echo "⚠️  You may need to manually review and import data"
    exit 1
fi

echo ""
echo "🎉 Migration completed successfully!"
echo ""
echo "Next steps:"
echo "1. Test your application with PostgreSQL"
echo "2. Keep data_backup.json as a backup"
echo "3. You can now deploy to production"
