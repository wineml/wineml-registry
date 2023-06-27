import { useEffect, useState } from 'react';
import serviceCaller from '../service';
import { useParams } from 'react-router-dom';
import Typography from '@mui/material/Typography';


function Model() {
    const [modelInfo, setModelInfo] = useState({});
    const [modelVersions, setModelVersions] = useState({});
    const params = useParams();
    let modelID = params.modelID;

    useEffect(() => {
        serviceCaller.get({
            route: `/model/${modelID}`,
            param: {}
        }).then((res) => {
            setModelInfo(res.data);
          }
        )
    }, [modelID]);


    return (
        <div className="Model">
            <Typography gutterBottom variant="h4" component="div" align='left'>
                {modelInfo.model_name}
            </Typography>
        </div>
    );
}

export default Model;
