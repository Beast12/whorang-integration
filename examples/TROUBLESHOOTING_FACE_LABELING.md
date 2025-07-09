# WhoRang Face Labeling Troubleshooting Guide

## Dashboard Fixed - Sensor Name Issues Resolved

✅ **All sensor references updated** to use the correct `sensor.whorang_ai_doorbell_*` naming pattern
✅ **Entity not found errors should be resolved** 
✅ **Conditional cards now reference correct sensors**

## Next Steps to Get Face Labeling Working

### 1. Check if Unknown Faces Sensor Exists
First, verify the sensor exists in Home Assistant:

**Go to:** Developer Tools → States  
**Look for:** `sensor.whorang_ai_doorbell_unknown_faces`

**If the sensor doesn't exist:**
- The integration may not be creating the unknown faces sensor
- Check Home Assistant logs for integration errors
- Restart Home Assistant to reload the integration

### 2. Add Required Helper Entities
The "Configuration error" messages are because you need to add helper entities to your `configuration.yaml`:

```yaml
# Add these to configuration.yaml
input_number:
  face_id_input:
    name: Face ID for Labeling
    min: 1
    max: 10000
    step: 1
    mode: box
    icon: mdi:identifier

input_text:
  person_name_input:
    name: Person Name for Labeling
    max: 100
    icon: mdi:account
    
  quick_person_name:
    name: Quick Person Name
    max: 100
    icon: mdi:account-fast
```

**After adding:** Restart Home Assistant

### 3. Test the Face Data Retrieval
Once the dashboard loads without errors:

1. **Click "Refresh Unknown Faces"** button
2. **Check if face data appears** in the "Unknown Face Details" section
3. **If no data appears:** Check the service call in Developer Tools

### 4. Manual Service Testing
Test the face labeling services manually:

**Go to:** Developer Tools → Services

**Test service:** `whorang.get_unknown_faces`
```yaml
service: whorang.get_unknown_faces
data:
  limit: 50
  quality_threshold: 0.6
```

**Expected result:** Should populate the unknown faces sensor with face data

### 5. Check Integration Logs
If services aren't working:

**Go to:** Settings → System → Logs  
**Look for:** WhoRang integration errors  
**Common issues:**
- API connection problems
- Service registration failures
- Backend API endpoint issues

### 6. Verify Backend API Endpoints
The integration needs these backend endpoints to work:
- `GET /api/detected-faces/unassigned` - Get unknown faces
- `POST /api/detected-faces/{id}/assign` - Label faces
- `GET /api/faces/persons` - Get known persons

**Test manually:** Visit `http://your-whorang-ip:3001/api/detected-faces/unassigned` in browser

### 7. Check Backend Logs
If API endpoints aren't working:
- Check WhoRang backend logs
- Verify face detection is working
- Ensure database has face data

## Expected Workflow After Fixes

1. **Dashboard loads without errors** ✅
2. **Click "Refresh Unknown Faces"** → Populates sensor with face data
3. **"Unknown Face Details" shows face information** → Face IDs, quality scores, image links
4. **Enter person name and click "Label Face"** → Successfully labels the face
5. **Face count decreases** → System learns the person

## Common Issues and Solutions

### Issue: "Unknown unknown face(s)" showing
**Cause:** Sensor exists but has no face data  
**Solution:** Click "Refresh Unknown Faces" to populate data

### Issue: No face details after refresh
**Cause:** Backend has no unlabeled faces or API error  
**Solution:** 
- Check backend for face detection data
- Verify API endpoints are working
- Check integration logs for errors

### Issue: Services not working
**Cause:** Integration services not properly registered  
**Solution:**
- Restart Home Assistant
- Check integration is properly installed
- Verify service definitions in Developer Tools

### Issue: Face images not loading
**Cause:** Image URLs not accessible  
**Solution:**
- Check if WhoRang backend is accessible from browser
- Verify image file paths exist on backend
- Check network connectivity

## Debug Steps

1. **Check sensor states** in Developer Tools → States
2. **Test services manually** in Developer Tools → Services  
3. **Review integration logs** in Settings → System → Logs
4. **Verify backend API** by testing endpoints directly
5. **Check face detection** is working in WhoRang backend

## Success Indicators

✅ Dashboard loads without "Entity not found" errors  
✅ "Refresh Unknown Faces" populates face data  
✅ Face details show with image links  
✅ Face labeling services work without errors  
✅ Face count decreases after successful labeling  

The dashboard configuration is now correct - the remaining issues are likely related to the integration setup, helper entities, or backend connectivity.
