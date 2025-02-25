export const Display = (props) => {
	let students = [
        {id: '49.104.001', name: 'Tèo'},
        {id: '49.104.003', name: 'Tý'}
    ];
	return (
    <div>
        <h2>{props.classId}</h2>
		{students.map((st) => {
			return <div key={st.id}>{st.id}, {st.name}</div>
		})
		}
	</div>
    )
};