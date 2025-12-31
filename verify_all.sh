#!/bin/bash

echo "=========================================="
echo "  VERIFICATION SCRIPT"
echo "=========================================="
echo ""

echo "1. Checking Database..."
echo "   Study Time:"
sqlite3 studypal.db "SELECT '   User ' || user_id || ': ' || total_study_time || ' minutes' FROM user_stats;"
echo ""

echo "2. Testing Search..."
python test_search.py 2>&1 | grep -E "(Testing:|✅|❌|PASSED|FAILED)" | head -10
echo ""

echo "3. Testing Study Time..."
python test_study_time.py 2>&1 | grep -E "(Testing|✅|❌|PASSED|FAILED|Total Study Time)" | head -10
echo ""

echo "=========================================="
echo "  SUMMARY"
echo "=========================================="
echo ""
echo "✅ Database: Check above for study time"
echo "✅ Search: Should show 'ALL TESTS PASSED'"
echo "✅ Time Tracking: Should show 'TEST PASSED'"
echo ""
echo "Next Step: Refresh profile page (Ctrl+F5)"
echo "Expected: Should show study time from database"
echo ""
echo "=========================================="
